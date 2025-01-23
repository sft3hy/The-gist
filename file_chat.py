import streamlit as st
import os
from helpers import extract_text
from config import DOC_SUMMARY_SYS_PROMPT, ALL_MODELS, OPENAI_MODELS, GROQ_MODELS, AZURE_API_KEY, GOOGLE_MODELS, GOOGLE_API_KEY
from groq import Groq
from openai import AzureOpenAI, OpenAI

st.title("Create your gist")

save_dir = "user_uploaded_files"
selected_files = []
file_paths = []

col1, col2 = st.columns(2)
with col2:
    st.markdown("LLM Temperature", help="Set the model temperature. 0 = more logical, 1.0 = more creative")
    temperature = st.slider(
                "A",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                label_visibility="collapsed"
                )
with col1:
    selected_model = st.selectbox(
                "Select a Gist creator LLM:",
                options = ALL_MODELS,
                index=ALL_MODELS.index("llama-3.3-70b-specdec"),
            )

uploaded_files = st.file_uploader(
            "Upload new file(s)",
            type=["txt", "pdf", "pptx"], 
            accept_multiple_files=True,
            key="main-file-uploader",
            label_visibility="collapsed"
        )
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Save uploaded files
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        selected_files.append(file_path)  # Treat uploaded files as selected

with st.expander("Or select uploaded data sources:", expanded=False):
    files = os.listdir(save_dir)
    for count, file in enumerate(files):
        file_path = os.path.join(save_dir, file)
        file_paths.append(file_path)
        
        if os.path.isfile(file_path):
            # Add a checkbox for each file
            is_selected = st.checkbox(f"📄 {file}", key=f"file_{count}")
            if is_selected:
                selected_files.append(file_path)

col1, col2, col3 = st.columns([1, 0.3, 1])
with col2:
    create_gist = st.button("Create Gist")


client = ""
if selected_model in OPENAI_MODELS:
    client_args = {
        "api_key": AZURE_API_KEY,
        "api_version": "2024-10-21",
        "azure_endpoint": "https://models.inference.ai.azure.com",
    }
    # remove keys with None values
    client_args = {k: v for k,
                        v in client_args.items() if v is not None}
    client = AzureOpenAI(**client_args)
elif selected_model in GROQ_MODELS:
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
elif selected_model in GOOGLE_MODELS:
    client = OpenAI(
                api_key=GOOGLE_API_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )


def stream_groq(stream):
    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text is not None and type(text) != "int":
            yield text

if temperature and selected_model and create_gist and selected_files:
    for file in selected_files:
        stream = client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": DOC_SUMMARY_SYS_PROMPT},
                    {"role": "user", "content": extract_text(file)},
                ],
                stream=True,
            )
        response = ""
        if selected_model in GROQ_MODELS:
            with st.chat_message("ai"):
                response = st.write_stream(stream_groq(stream))
        else:
            with st.chat_message("ai"):
                response = st.write_stream(stream)
