import os
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("RAG-Based Customer Support Assistant")

    # Load vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="data/chroma_db", embedding_function=embeddings)

    # Create instruction-tuned LLM
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_length=256,
        temperature=0.2,
    )
    llm = HuggingFacePipeline(pipeline=pipe)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
    )

    query = st.text_input("Ask a question:")

    if query:
        answer = qa_chain.run(query)
        st.write("Answer:", answer.strip())

if __name__ == "__main__":
    main()