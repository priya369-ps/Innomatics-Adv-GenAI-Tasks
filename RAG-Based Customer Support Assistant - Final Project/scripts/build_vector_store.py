import os
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def build_vector_store():
    # Load documents
    with open("data/faq.txt", "r") as f:
        text = f.read()
    documents = [Document(page_content=text, metadata={"source": "faq.txt"})]

    # Split documents
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create vector store
    vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="data/chroma_db")

    print("Vector store built and persisted.")

if __name__ == "__main__":
    build_vector_store()