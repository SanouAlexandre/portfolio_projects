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

def call_langflow_api(prompt: str, 
                      input_type: str = "chat", 
                      output_type: str = "chat") -> Optional[Dict[str, Any]]:
    payload = {
        "input_value": prompt,
        "output_type": output_type,
        "input_type": input_type
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
        return {
            "response": response.json(),
            "payload": payload
        }

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse API response: {str(e)}")
        return None

# Streamlit UI
st.title("LangFlow API Integration")
st.markdown("""
This app connects to your LangFlow workflow to process natural language inputs.
""")

# User input
user_input = st.text_area("Enter your message:", "hello world!")
input_type = st.selectbox("Input type:", ["chat", "query", "command"])
output_type = st.selectbox("Output format:", ["chat", "json", "text"])

if st.button("Process"):
    with st.spinner("Calling LangFlow API..."):
        result_data = call_langflow_api(
            prompt=user_input,
            input_type=input_type,
            output_type=output_type
        )

        if result_data:
            result = result_data["response"]
            payload = result_data["payload"]

            st.success("API call successful!")

            # Output
            if output_type == "json":
                st.json(result)
            else:
                text = result.get("text") or result.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text")
                st.write(text or str(result))

            # Debug section
            with st.expander("Debug Info"):
                st.code(f"API URL: {API_URL}")
                st.code(f"Request payload: {json.dumps(payload, indent=2)}")
                st.code(f"Full response: {json.dumps(result, indent=2)}")

# Sidebar with configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", API_URL)
    if api_url != API_URL:
        API_URL = api_url
        st.rerun()