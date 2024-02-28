# 3GPP-RAG-chat README

## Overview

The 3GPP-RAG-chat project is a weekend project for processing, analyzing and chatting with documents from the ETSI and 3GPP standards LOCALLY. I utilized libraries for Retrieval Augmented Generation (RAG)-powered Large Language Models (LLMs) such as Ollama and llama-index. This project needs a NVIDIA GPU with at least 12 GB VRAM.


## Quick Demo
https://github.com/saria-lh/3GPP-RAG-chat/assets/139324475/91ffa295-9ce5-45f6-8967-2d6e65989c57


## Installation

Ensure you have Python 3.x installed on your system. Then, follow these steps to install the necessary dependencies:

### Llama-Index

Install `PyMuPDF`, `ChromaDB`, `llama-index` and its related packages using pip:

```bash
pip install llama-index PyMuPDF chromadb
pip install llama-index-core llama-index-readers-file llama-index-llms-ollama llama-index-embeddings-huggingface
```

### Ollama

Install `Ollama` using the provided script and pip:

```bash
curl -fsSL https://ollama.com/install.sh | sh
pip install ollama
```

### LLM Pull with Ollama

We will be utilizing `int8` quantized mistral 7b-instruct model. Use the `ollama_pull.py` script to pull the  model:

```bash
python3 ollama_pull.py -m mistral:7b-instruct-v0.2-q8_0
```

## Usage

All you need to start querying is to download the index data `3gpp_db` from [here](https://queensuca-my.sharepoint.com/:u:/g/personal/20msa7_queensu_ca/Eai8TFKg_W1Apv6sDlKAvhkBMuC7RCT_CUMahDIkqZH1Tg), and go to step 4. Or you can start from scratch and begin the document scraping and processing workflow with the following steps:

1. **Downloading Documents**: Execute the `download.py` script to initiate the download of all PDF files from the ETSI website. Note that this process may take several hours to complete.

    ```bash
    python download.py
    ```

2. **Cleaning Documents**: Run the `clean.py` script to remove any duplicate files and older versions of documents, ensuring that only the most relevant and up-to-date documents are kept for analysis. To save time, documents and folders are made available [here](https://queensuca-my.sharepoint.com/:u:/g/personal/20msa7_queensu_ca/EaYDRfFlgXNFhubyxpZTrOUB5bg38U-KgQBAARbdI2Rp-Q).

    ```bash
    python clean.py
    ```

3. **Indexing Documents**: Use the `index.py` script to index all documents. This step is crucial for efficiently searching and retrieving information from the documents later on. To save time, the index is available available [here](https://queensuca-my.sharepoint.com/:u:/g/personal/20msa7_queensu_ca/Eai8TFKg_W1Apv6sDlKAvhkBMuC7RCT_CUMahDIkqZH1Tg).

    ```bash
    python index.py
    ```

4. **Querying Documents**: Finally, execute the `query.py` script to start querying the indexed documents. This allows you to search for specific information within the vast collection of ETSI and 3GPP documents.

    ```bash
    python query.py
    ```


## TODO

- [ ] Wrap the code within a Dockerfile for containerized deployment.
- [ ] Improve the retrieval process, possibly integrating late interaction mechanisms such as ColBERT for enhanced efficiency and accuracy.
- [ ] Add UI, possibly with Gradio or Streamlit.

## Contribution

Contributions are welcome! If you'd like to improve the project or suggest new features, please feel free to submit a pull request or open an issue.
