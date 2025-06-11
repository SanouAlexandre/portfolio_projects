import requests
import streamlit as st
from dotenv import load_dotenv
import os
import json
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv()

# Configuration
API_URL = os.getenv("LANGFLOW_API_URL")
API_TIMEOUT = int(os.getenv("API_TIMEOUT"))  # seconds

def call_langflow_api(prompt: str) -> Optional[Dict[str, Any]]:
    payload = {
        "input_value": prompt,
        "output_type": "chat",  # fixed
        "input_type": "chat"    # fixed
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('LANGFLOW_API_KEY')}"
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse API response: {str(e)}")
        return None

# Streamlit UI
st.title("LangFlow Chat Interface")
st.markdown("Send a message to your LangFlow-powered assistant.")

# User input
user_input = st.text_area("Your message:", "hello world!")

if st.button("Send"):
    with st.spinner("Contacting LangFlow..."):
        result = call_langflow_api(prompt=user_input)

        if result:
            st.success("✅ API call successful!")

            # Extract and show chat response
            text = result.get("text") or \
                   result.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text")

            st.markdown("**Response:**")
            st.write(text or str(result))

# Sidebar with links and description
with st.sidebar:
    st.header("🔗 Connect with Me")
    st.markdown("[GitHub](https://github.com/SanouAlexandre)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/alexandre-sanou-bb3b74101/)")

    st.markdown("---")  # horizontal separator

    st.header("📝 About This App")
    st.markdown("""
    This application leverages **LangFlow** combined with the power of the **DataStax Astra** database to deliver intelligent, context-aware responses to customer inquiries. By utilizing **Retrieval-Augmented Generation (RAG)** on rich datasets such as FAQs, order history, and product information, the app provides precise and relevant answers tailored to customer support needs.

    Designed as a practical tool for customer service teams, it enhances user experience by enabling quick access to critical information and streamlining the support process. Whether it’s clarifying product details, tracking orders, or addressing common questions, this app empowers support agents and customers alike with real-time, data-driven assistance.
    """)

