from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .integrations.openrouter import OpenRouter
from db.db import DokuragDB

class DokuragChain:
    """A LangChain chain that uses OpenRouter LLM for document Q&A."""
    
    def __init__(self, documents_folder: str | None = None):
        """Initialize the chain with OpenRouter LLM.
        
        Args:
            documents_folder: Optional path to a folder containing documents for future retrieval.
        """
        self.llm = OpenRouter()
        
        # Default prompt template for document Q&A
        default_template = """You are a technical support assistant. Answer the question or respond with relevant information.

        Question: {question}

        Answer:"""
        
        self.basic_prompt = PromptTemplate.from_template(default_template)

        rag_template = """You are a technical support assistant. Answer the question or respond with relevant information based on the context provided, which is retrieved from technical documents.

        Context: {context}

        Question: {question}

        Answer:"""
        
        self.rag_prompt = PromptTemplate.from_template(rag_template)
        
        # Create the chain: prompt -> llm -> output parser
        self.basic_chain = (
            self.basic_prompt 
            | self.llm 
            | StrOutputParser()
        )

        self.rag_chain = (
            self.rag_prompt 
            | self.llm 
            | StrOutputParser()
        )

        self.db = DokuragDB(documents_folder=documents_folder)
    
    def invoke(self, question: str, documents: list[str] | None = None) -> str:
        """Invoke the chain with a question and optional context.
        
        Args:
            question: The question to ask
            documents: Optional list of document paths to include as context

            
        Returns:
            The LLM's response
        """
        context_docs = []

        if documents:
            # Load provided docs and build retrieval context
            self.db.load_documents(uploaded_documents=documents)
            context_docs = self.db.query_vectors(question) or []

        return self.rag_chain.invoke({
            "question": question,
            "context": "\n\n".join([doc.page_content for doc in context_docs])
        })
    
    def simple_invoke(self, prompt: str) -> str:
        """Simple invoke method that sends a direct prompt to the LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            
        Returns:
            The LLM's response
        """
        return self.basic_chain.invoke({"question": prompt})
