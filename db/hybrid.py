import os
import io
import re
import hashlib
import uuid
from queue import Queue
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.config import Property, DataType, Configure
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

"""
This class is a wrapper for Weaviate with hybrid (BM25 + vector) search.

Simple supported functions:
- add_vectors
- embed_documents
- query_vectors -> Hybrid retrieval combining BM25 and vector similarity

Simple flow of loading documents:

load documents -> check type -> chunk -> process chunks

"""
class HybridDB:

    def __init__(self, documents_folder: str | None = None):
        self.setup(documents_folder)

    # class vars setup
    def setup(self, documents_folder: str | None = None):

        load_dotenv()

        # Select embedding model (default: 768 dims)
        embedding_model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

        embedding_function = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            encode_kwargs={"normalize_embeddings": True},
        )

        # diff models need diff dirs to avoid dimension mismatch - BAAI -> 768 dims / allminilm -> 384 dims
        safe_model_dir = re.sub(r"[^A-Za-z0-9._-]+", "_", embedding_model_name)
        persist_directory = os.path.join("chroma_storage", safe_model_dir)

        # Keep the embedder handy
        self.embedder = embedding_function

        # Weaviate setup
        conn = ConnectionParams.from_params(
            http_host="localhost",
            http_port=8089,
            http_secure=False,
            grpc_host="localhost",
            grpc_port=50051,
            grpc_secure=False
        )   
        self.client = weaviate.WeaviateClient(
            connection_params=conn,
            additional_config=AdditionalConfig(
                timeout=Timeout(init=5, query=30, insert=60)
            )
        )
        
        self.collection_name = os.getenv("WEAVIATE_COLLECTION", "Dokurag_docs")
        self._ensure_collection()

        self.splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        self.documents_folder = documents_folder

    # Ensure collection exists with proper schema
    def _ensure_collection(self):

        try:
            self.client.connect()

            # In weaviate-client v4, list_all returns a list of collection names (strings)
            existing = list(self.client.collections.list_all())
            print(existing)
            if self.collection_name in existing:
                return

            self.client.collections.create(
                name=self.collection_name,
                description="Dokurag document chunks",
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="page", data_type=DataType.INT),
                    Property(name="type", data_type=DataType.TEXT),
                ],
            )
            print(f"Collection {self.collection_name} created successfully.")

        except Exception as e:
            print(f"Error connecting to Weaviate: {e}")
            raise e
        finally:
            self.client.close()
        

    # Hybrid search over BM25 + vector
    def query_vectors(self, query: str, k: int = 40, alpha: float = 0.5):
        
        try:
            self.client.connect()

            collection = self.client.collections.get(self.collection_name)
            query_vector = self.embedder.embed_query(query)
            result = collection.query.hybrid(
                query=query,
                vector=query_vector,
                alpha=alpha,
                limit=k,
                return_properties=["text", "source", "page", "type"],
            )
            documents: list[Document] = []
            for obj in result.objects:
                props = obj.properties or {}
                page_content = props.get("text", "")
                metadata = {
                    "source": props.get("source"),
                    "page": props.get("page"),
                    "type": props.get("type"),
                }
                documents.append(Document(page_content=page_content, metadata=metadata))
            return documents

        except Exception as e:
            print(f"Error querying Weaviate: {e}")
            raise e
        finally:
            self.client.close()
    
    # Hash chunk to use as id - helper function for removing duplicates
    def hash_chunk(self, chunk: str):
        return hashlib.sha256(chunk.encode()).hexdigest()
    
    # Get file names and retrieve only non-pdf files - modeular func for loading function
    def source_files(self):

        all_files = sorted([os.path.join(self.documents_folder, f) for f in os.listdir(self.documents_folder) if os.path.isfile(os.path.join(self.documents_folder, f))])

        for file in all_files:
            if not file.endswith(".pdf"):
                all_files.remove(file)
                continue

        return all_files

    """
    This function loads docs to db

    batch_size: int = 10 -> batch size for uploading documents
    uploaded_documents: list[Document] -> use documents provided
    """
    def load_documents(self, batch_size: int = 10, uploaded_documents: list[str] | None = None):
        all_files = (
            uploaded_documents
            if uploaded_documents is not None and len(uploaded_documents) > 0
            else self.source_files()
        )

        if not all_files:
            print("No PDF files found to process.")
            return

        for batch_start in range(0, len(all_files), batch_size):
            batch_files = all_files[batch_start:batch_start + batch_size]
            docs_to_add = []
            doc_ids = []

            for file_path in batch_files:
                doc = fitz.open(file_path)

                for page_index, page in enumerate(doc):
                    # extract and chunk text
                    text = page.get_text().strip()
                    if text:
                        text_chunks = self.splitter.split_text(text)
                        for chunk in text_chunks:
                            docs_to_add.append(Document(
                                page_content=chunk,
                                metadata={"source": os.path.basename(file_path), "page": page_index + 1, "type": "text"}
                            ))
                            doc_ids.append(str(uuid.uuid5(uuid.NAMESPACE_URL, chunk)))
                    
            try:
                self.client.connect()
                collection = self.client.collections.get(self.collection_name)
                for doc, id_ in zip(docs_to_add, doc_ids):
                    try:
                        vector = self.embedder.embed_query(doc.page_content)
                        collection.data.insert(
                            properties={
                                "text": doc.page_content,
                                "source": doc.metadata.get("source"),
                                "page": doc.metadata.get("page"),
                                "type": doc.metadata.get("type"),
                            },
                            vector=vector,
                            uuid=id_,
                        )
                    except Exception as e:
                        if "already exists" in str(e) or "duplicate" in str(e):
                            continue
                        else:
                            raise e
            finally:
                self.client.close()

            print(f"✅ Uploaded {len(batch_files)} documents with {len(docs_to_add)} chunks.")