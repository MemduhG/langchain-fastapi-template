from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from os import listdir, path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain_core.documents.base import Document
from langchain_core.vectorstores.base import VectorStore
from langchain_core.runnables.base import Runnable
import argparse

load_dotenv()


def load_documents(folder: str = "./documents") -> list[Document]:
    docs = []
    for item in listdir(folder):
        loader = TextLoader(path.join(folder, item))
        docs.extend(loader.load())
    return docs


def populate_vector_db(docs: list[Document], db_path: str = "vectors") -> VectorStore:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
    vector.save_local(db_path)
    return vector


def load_vector_db(db_path: str = "vectors") -> VectorStore:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
    return db


def get_retrieval_chain() -> Runnable:
    prompt = ChatPromptTemplate.from_template(
        """Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}"""
    )
    llm = ChatOpenAI()
    document_chain = create_stuff_documents_chain(llm, prompt)

    vector = load_vector_db()
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", type=str, default="vectors")
    parser.add_argument("--document-folder", type=str, default="./documents")
    parser.add_argument("--repopulate", action="store_true", default=False)

    args = parser.parse_args()
    if path.exists(args.db_path) and args.repopulate is False:
        print(f"The vector DB path '{args.db_path}' already exists. Run with option --repopulate to force repopulation.")
        exit()

    print("Loading documents...")
    docs = load_documents(args.document_folder)
    print("Populating vector DB...")
    populate_vector_db(docs, args.db_path)
