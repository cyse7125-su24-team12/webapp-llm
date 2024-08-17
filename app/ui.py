import streamlit as st
import requests
# from .model import generate_response
import os

model_name = os.getenv("MODEL_NAME")

st.title("Chat with CVE-LLM")

# User input area (Question box)
user_input = st.text_area("Your Question:", key="input", height=100)

# Answer display area (Answer box)
answer_placeholder = st.empty()

# Send user input to the Flask API and display the response in the Answer box
if st.button("Send") and user_input:
    response = requests.post(
        "http://localhost:5000/generate",
        json={
            "model": model_name,
            "prompt": user_input,
            "stream": False
        }
    )
    # response = generate_response(user_input)
    response_data = response.json()
    answer = response_data.get("response",{}).get("result", "No response received.")
    
    # Display the answer in the Answer box
    answer_placeholder.text_area("Answer:", value=answer, height=300)

