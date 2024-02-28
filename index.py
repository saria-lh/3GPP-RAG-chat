import os
import fitz
import ollama
import chromadb
from tqdm import tqdm
from llama_index.core import Document
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

main_dir = './unique_pdfs'
create_dir_path = lambda main_dir, sub_dir: os.path.join(main_dir, sub_dir)
get_full_path_files = lambda dir_path: [os.path.join(dir_path, file) for file in os.listdir(dir_path)]

def get_documents_as_str(dir_files: list) -> list:
    """
    Extracts and concatenates text from documents in the specified directory files list.
    
    Args:
        dir_files (list): A list of file paths from which to extract text.
    
    Returns:
        list: A list where each element contains the concatenated text of a document.
    """
    doc_list = []
    for fname in tqdm(dir_files):
        with fitz.open(fname) as doc:  # open document
            text = chr(12).join([page.get_text() for page in doc])
            doc_list.append(text)
    return doc_list

def index_documents(db_path: str, collection_name: str, documents):
    """
    Indexes documents in a ChromaDB collection using a vector store index.
    
    This function creates or retrieves a ChromaDB collection, assigns a ChromaVectorStore as the vector 
    store to the storage context,and then indexes the provided documents. The indexing process involves
    creating embeddings for the documents and storing these embeddings in the vector store for later retrieval 
    and similarity search.
    
    Args:
        db_path (str): The file system path where the ChromaDB database to be stored.
        collection_name (str): The name of the collection within ChromaDB where the documents are to be indexed.
        documents (list): A list of documents to be indexed. Each document should be a Document object.
    
    Returns:
        VectorStoreIndex: An index object that represents the indexed documents and their embeddings within the 
        specified collection in ChromaDB.
    
    """
    db = chromadb.PersistentClient(path=db_path)
    chroma_collection = db.get_or_create_collection(collection_name)

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # create your index
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True
    )
    return index

def read_indexed_documents(db_path: str, collection_name: str):
    """
    Loads an existing index from a ChromaDB collection using a vector store index.
    
    This function accesses a specified ChromaDB collection and uses the associated ChromaVectorStore as the 
    vector store within the given storage context to load an index of previously indexed documents. This is 
    useful for retrieving and querying the index without needing to re-index the documents.
    
    Args:
        db_path (str): The file system path to the ChromaDB database where the collection with the indexed documents is stored.
        collection_name (str): The name of the collection within ChromaDB from which to load the indexed documents.
    
    Returns:
        VectorStoreIndex: An index object loaded from the specified collection in ChromaDB, containing the embeddings
         and the documents indexed in that collection.

    """
    db = chromadb.PersistentClient(path=db_path)
    chroma_collection = db.get_or_create_collection(collection_name)

    # assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(
        storage_context=storage_context, vector_store=vector_store,show_progress=True
    )
    return index

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5", trust_remote_code=True, embed_batch_size=10)

ts_dir = create_dir_path(main_dir, 'ts')
tr_dir = create_dir_path(main_dir, 'tr')
es_dir = create_dir_path(main_dir, 'es')
en_dir = create_dir_path(main_dir, 'en')

ts_dir_files = get_full_path_files(ts_dir)
tr_dir_files = get_full_path_files(tr_dir)
es_dir_files = get_full_path_files(es_dir)
en_dir_files = get_full_path_files(en_dir)

ts_docs_str = get_documents_as_str(ts_dir_files)
tr_docs_str = get_documents_as_str(tr_dir_files)
es_docs_str = get_documents_as_str(es_dir_files)
en_docs_str = get_documents_as_str(en_dir_files)

ts_documents = [Document(text=ts, metadata={"filename": ts_id}) for ts, ts_id in zip(ts_docs_str,ts_dir_files)]
tr_documents = [Document(text=tr, metadata={"filename": tr_id}) for tr, tr_id in zip(tr_docs_str,tr_dir_files)]
es_documents = [Document(text=es, metadata={"filename": es_id}) for es, es_id in zip(es_docs_str,es_dir_files)]
en_documents = [Document(text=en, metadata={"filename": en_id}) for en, en_id in zip(en_docs_str,en_dir_files)]

#----------------------- You can also use presist to save the index -------------------------#
# vector_index = VectorStoreIndex.from_documents(ts_Documents, show_progress=True)
# vector_index.storage_context.persist('./index_ts')
#--------------------------------------------------------------------------------------------#

ts_index = index_documents(db_path='3gpp_db', collection_name='ts_docs', documents=ts_documents)
tr_index = index_documents(db_path='3gpp_db', collection_name='tr_docs', documents=tr_documents)
es_index = index_documents(db_path='3gpp_db', collection_name='es_docs', documents=es_documents)
en_index = index_documents(db_path='3gpp_db', collection_name='en_docs', documents=en_documents)
