# 3GPP-RAG-chat README

## Overview

The 3GPP-RAG-chat project is a weekend project for processing, and analyzing documents from the ETSI and 3GPP standards. I utilized libraries for Retrieval Augmented Generation (RAG)-powered Large Language Models (LLMs) such as Ollama and llama-index. This project needs a NVIDIA GPU with at least 12 GB VRAM.


## Quick Demo
https://github.com/saria-lh/3GPP-RAG-chat/assets/139324475/91ffa295-9ce5-45f6-8967-2d6e65989c57


## Installation

Ensure you have Python 3.x installed on your system. Then, follow these steps to install the necessary dependencies:

### Llama-Index

Install `llama-index` and its related packages using pip:

```bash
pip install llama-index
pip install llama-index-core llama-index-readers-file llama-index-llms-ollama llama-index-embeddings-huggingface
```

### Ollama

Install `Ollama` using the provided script and pip:

```bash
curl -fsSL https://ollama.com/install.sh | sh
pip install ollama
```

### Model Pull

Use the `ollama_pull.py` script to pull the required model:

```bash
python3 ollama_pull.py -m mistral:7b-instruct-v0.2-q8_0
```

## Usage

After completing the installation process, you can begin the document scraping and processing workflow with the following steps:

1. **Downloading Documents**: Execute the `download.py` script to initiate the download of all PDF files from the ETSI website. Note that this process may take several hours to complete. To save time, pre-downloaded documents and folders are made available at [link coming soon](#LINK).

    ```bash
    python download.py
    ```

2. **Cleaning Documents**: Run the `clean.py` script to remove any duplicate files and older versions of documents, ensuring that only the most relevant and up-to-date documents are kept for analysis.

    ```bash
    python clean.py
    ```

3. **Indexing Documents**: Use the `index.py` script to index all documents. This step is crucial for efficiently searching and retrieving information from the documents later on.

    ```bash
    python index.py
    ```

4. **Querying Documents**: Finally, execute the `query.py` script to start querying the indexed documents. This allows you to search for specific information within the vast collection of ETSI and 3GPP documents.

    ```bash
    python query.py
    ```

Follow these steps to effectively utilize the 3GPP-RAG-chat project for your document processing needs. Further details and advanced usage instructions will be provided in the comprehensive documentation available in the subsequent sections.


## TODO

- [ ] Wrap the code within a Dockerfile for containerized deployment.
- [ ] Improve the retrieval process, possibly integrating late interaction mechanisms such as ColBERT (late interaction) for enhanced efficiency and accuracy.
- [ ] Add UI, possible with Gradio or Streamlit.

## Contribution

Contributions are welcome! If you'd like to improve the project or suggest new features, please feel free to submit a pull request or open an issue.
