import os
from tempfile import NamedTemporaryFile

from src.utils.s3_helper import download_file, upload_index, download_index
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


def build_store(s3_keys, index_key=None, download_dir="/tmp"):
    """Download resumes from S3, split into chunks, and create/load a FAISS store."""
    if index_key:
        tmp_idx = os.path.join(download_dir, "faiss.index")
        try:
            download_index(index_key, tmp_idx)
            return FAISS.load_local(tmp_idx, OpenAIEmbeddings())
        except Exception:
            pass
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
    store = FAISS.from_documents(chunks, embeddings)
    if index_key:
        with NamedTemporaryFile(delete=False) as tmp:
            store.save_local(tmp.name)
            upload_index(tmp.name, index_key)
    return store
