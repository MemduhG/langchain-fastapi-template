from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from os import listdir, path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


load_dotenv()

def load_documents(folder="./documents"):
    docs = []
    for item in listdir(folder):
        loader = TextLoader(path.join(folder, item))
        docs.extend(loader.load())
    return docs


def populate_vector_db(docs, db_path="vectors.db"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
    vector.save_local(db_path)
    return vector


def load_vector_db(db_path="vectors.db"):
    db = FAISS.load_local(db_path)
    return db


if __name__ == "__main__":
    docs = load_documents()
    populate_vector_db(docs)
    pass
