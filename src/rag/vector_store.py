from src.utils.s3_helper import download_file
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


def build_store(s3_keys, download_dir="/tmp"):
    """Download resumes from S3, split into chunks, and create a FAISS store."""
    local_paths = []
    for key in s3_keys:
        local_path = f"{download_dir}/{key.replace('/', '_')}"
        download_file(key, local_path)
        local_paths.append(local_path)

    docs = []
    for path in local_paths:
        docs.extend(TextLoader(path).load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(chunks, embeddings)
