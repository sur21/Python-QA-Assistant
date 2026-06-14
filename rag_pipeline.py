from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class PythonQARAG:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)
        self.vectorstore = None
        self.retriever = None
        self.chain = None

    def build_index(self, documents):
        print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
        splits = text_splitter.create_documents(
            [doc["page_content"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents]
        )
        
        print(f"Building vector store with {len(splits)} chunks...")
        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 6})
        self._build_chain()
        print("Index built successfully!")

    def load_index(self):
        self.vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 6})
        self._build_chain()

    def _build_chain(self):
        template = """You are an expert Python tutor for data science learners.
Answer ONLY using the provided context from Stack Overflow. 
Be clear, educational, and include code snippets when helpful.

Context:
{context}

Question: {question}

Answer:"""

        prompt = ChatPromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n---\n\n".join(doc.page_content for doc in docs)

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str):
        if not self.chain:
            self.load_index()
        return self.chain.invoke(question)
