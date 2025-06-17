import os
from tempfile import NamedTemporaryFile

from src.utils.s3_helper import download_file, upload_index, download_index
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, OpenSearchVectorSearch
from langchain.embeddings import OpenAIEmbeddings


def build_store(s3_keys, index_key=None, download_dir="/tmp"):
    """Download resumes from S3, split into chunks, and create/load a vector store."""

    opensearch_endpoint = os.getenv("OPENSEARCH_ENDPOINT")
    if opensearch_endpoint and index_key:
        try:
            return OpenSearchVectorSearch(
                opensearch_url=opensearch_endpoint,
                index_name=index_key,
                embedding_function=OpenAIEmbeddings().embed_query,
            )
        except Exception:
            pass
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

    if opensearch_endpoint and index_key:
        store = OpenSearchVectorSearch.from_documents(
            chunks,
            embeddings,
            opensearch_url=opensearch_endpoint,
            index_name=index_key,
        )
        return store

    store = FAISS.from_documents(chunks, embeddings)
    if index_key:
        with NamedTemporaryFile(delete=False) as tmp:
            store.save_local(tmp.name)
            upload_index(tmp.name, index_key)
    return store
