import os
import io
import re
import hashlib
from queue import Queue
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

"""
This class is a wrapper for the ChromaDB in the langchain way.

Simple supported functions:
- add_vectors
- embed_documents
- query_vectors -> search for similar vectors then rerank usiong mmr

Simple flow of loading documents:

load documents -> check type -> chunk -> process chunks

"""
class DokuragDB:
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

        self.db = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
        self.retriever = self.db.as_retriever(search_type="mmr", search_kwargs={"k": 40, "lambda_mult": 0.3})
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        self.documents_folder = documents_folder

    # simple retriever invoking - FUTURE: maybe remove
    def query_vectors(self, query: str):
        return self.retriever.invoke(query)
    
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
                            doc_ids.append(self.hash_chunk(chunk))
                    
            for doc, id_ in zip(docs_to_add, doc_ids):
                try:
                    self.db.add_documents([doc], ids=[id_])
                except Exception as e:
                    if "found duplicates" in str(e):
                        #print(f"Duplicate chunk found: {id_}") # FUTURE: log this to central db log
                        continue
                    else:
                        raise e

            print(f"✅ Uploaded {len(batch_files)} documents with {len(docs_to_add)} chunks.")