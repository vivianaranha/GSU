import streamlit as st
import requests

st.set_page_config(page_title="AI App with Streamlit + FastAPI", layout="centered")
st.title("🧠 Build an AI App with DeepSeek")
st.write("Type a prompt below and get a smart response from DeepSeek running via Ollama.")

prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Generate Response"):
    if prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Talking to the AI..."):
            try:
                response = requests.post("http://localhost:8000/generate", json={"prompt": prompt})
                result = response.json()
                st.markdown("### 💬 AI Response")
                st.success(result["response"])
            except Exception as e:
                st.error(f"Error: {str(e)}")
