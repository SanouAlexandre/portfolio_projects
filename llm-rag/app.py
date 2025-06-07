import glob
import os

import chromadb
import streamlit as st
from openai import OpenAI
from sentence_transformers import CrossEncoder

# Constants
BASE_DATA_DIR = "data/wiki"
COLLECTION_NAME = "test"
N_QUERY_RESULTS = 3

# Set OpenAI API Key
client = OpenAI()

# Streamlit UI customization
st.markdown(
    """
    <style>
    div[data-testid="column"] {
        width: fit-content !important;
        flex: unset;
    }
    div[data-testid="column"] * {
        width: !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to load a single text document
def _load_single_document(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

# Load all documents from the base directory
@st.cache_data
def load_documents(base_dir):
    filenames = glob.glob(f"{base_dir}/*.txt")
    return [_load_single_document(filename) for filename in filenames]

# Load and initialize ChromaDB collection
@st.cache_resource
def load_chromadb(name, documents):
    client = chromadb.Client()
    ids = list(map(str, range(len(documents))))
    collection = client.create_collection(name)
    collection.add(ids=ids, documents=documents)
    return collection

# Load the sentence transformer ranking model
@st.cache_resource
def load_ranker_model(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
    return CrossEncoder(model_name)

# Function to call OpenAI's Chat API (v1 style)
def rag(query, documents, model="gpt-3.5-turbo"):
    information = "\n\n".join(documents)
    messages = [
        {
            "role": "system",
            "content": (
                "Use the following information to answer the user's question. "
                "Answer the question using only this information. "
                "If you don't know the answer, just say that you don't know."
            ),
        },
        {"role": "user", "content": f"Question: {query}\n\nInformation: {information}"}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content

# Main Streamlit application
if __name__ == '__main__':
    st.title("LLM + RAG Demo Application")

    query = st.text_input("Enter your question here:")
    documents = load_documents(BASE_DATA_DIR)
    collection = load_chromadb(COLLECTION_NAME, documents)
    ranker_model = load_ranker_model()

    col_1, col_2 = st.columns([1, 1])
    with col_1:
        btn_submit = st.button("Submit")
    with col_2:
        cb_display_retrieved_documents = st.checkbox("Display the retrieved documents")

    if btn_submit and query:
        results = collection.query(
            query_texts=[query],
            n_results=N_QUERY_RESULTS,
        )['documents'][0]

        # Rank results using the cross-encoder
        pairs = [[query, result] for result in results]
        ranker_scores = ranker_model.predict(pairs)
        results = [result for _, result in sorted(zip(ranker_scores, results), reverse=True)]

        result = rag(query, documents=results)
        st.write(result)

        if cb_display_retrieved_documents:
            st.write(results)
