import streamlit as st
from ollama import Client

# 1. Connect to your separate Ollama container
client = Client(host='http://ollama:11434')

st.title("Ollama WebUI")

# 2. Fetch pre-installed models for the dropdown
try:
    models_info = client.list()
    model_names = [m['name'] for m in models_info['models']]
except Exception as e:
    st.error(f"Could not connect to Ollama: {e}")
    model_names = []

# Sidebar for model selection
selected_model = st.sidebar.selectbox("Select Model", model_names)

# Initialize empty chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display current chat history (will be empty on first load)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Start chatting (no pre-existing prompt)
if prompt := st.chat_input("Enter your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat(
            model=selected_model,
            messages=st.session_state.messages,
            stream=True,
        )
        # Writes the response as it streams from the container
        response = st.write_stream(chunk['message']['content'] for chunk in stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
