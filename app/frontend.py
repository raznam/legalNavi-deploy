import streamlit as st
import requests

# Streamlit UI
st.title("LegalNavi AI Model")
st.write("Enter a crime narration below to analyze it.")

# Input Text Area
narration_input = st.text_area("Crime Narration", placeholder="Describe the crime incident here...")

# Backend URL
backend_url = "http://127.0.0.1:8000/process-narration"

# Submit Button
if st.button("Submit"):
    if narration_input.strip():
        try:
            # Send the request to the FastAPI backend
            response = requests.post(backend_url, json={"narration": narration_input})
            
            if response.status_code == 200:
                data = response.json()
                st.write("### AI Response:")
                st.write(data["response"])
                st.write(f"**Latency:** {data['latency']}")
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Error: Unable to connect to the backend. {e}")
    else:
        st.error("Please enter a narration.")
