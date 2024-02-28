
import ollama
import chromadb
import time
from transformers import AutoTokenizer
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def typewriter_effect(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

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

#--------------------------------READING----------------------------------#

if __name__ == "__main__":

    ts_index = read_indexed_documents(db_path='3gpp_db', collection_name='ts_docs')
    tr_index = read_indexed_documents(db_path='3gpp_db', collection_name='tr_docs')
    es_index = read_indexed_documents(db_path='3gpp_db', collection_name='es_docs')
    en_index = read_indexed_documents(db_path='3gpp_db', collection_name='en_docs')

    model = "mistral:7b-instruct-v0.2-q8_0"
    Settings.llm = Ollama(model=model)
    Settings.tokenizer = AutoTokenizer.from_pretrained(
        "mistralai/Mistral-7B-Instruct-v0.2"
    )

    try:
        resp = Settings.llm.complete("Hello!")
        # print(resp)
        print('LLM Loaded!')
    except Exception as e:
        print(e)
        try:
            ollama.pull(model)
        except:
            raise NotImplementedError


    query_engine = ts_index.as_query_engine()
    print('Ask anything you want! Currently only Supporting Techincal Specification Documents.')
    while True:
        print('-->')
        query = input()
        response = query_engine.query(query)
        typewriter_effect(response.response)
        print()
        metadata = response.metadata
        top_file_id = list(metadata.keys())[0]
        print('Relevant file: ',response.metadata[top_file_id]['filename'])