import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def extract_text_from_pdfs(uploaded_files) -> str:
    text = ""
    for f in uploaded_files:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text += page_text + "\n"
    return text

def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n", " ", ""]
    )
    return splitter.split_text(text)


def build_vectorstore(chunks, api_key: str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
    return FAISS.from_texts(chunks, embeddings)


def build_conv_chain(vs, api_key: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vs.as_retriever(), memory=memory
    )


def show_chat(history):
    for msg in history:
        role = "user" if msg.type == "human" else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

load_dotenv()
st.set_page_config(page_title="Chat with multiple PDFs", page_icon="📚")

if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.header("Chat with multiple PDFs 📚")
st.write("Upload PDFs in the sidebar, click **Process**, then ask a question.")

with st.sidebar:
    st.subheader("Your documents")
    files = st.file_uploader(
        "Upload your PDFs here and click 'Process'",
        type=["pdf"],
        accept_multiple_files=True,
    )
    process = st.button("Process")

    if process:
        if not files:
            st.warning("Please upload at least one PDF.")
        else:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                st.error("OPENAI_API_KEY missing. Add it to a .env file and restart.")
            else:
                with st.spinner("Processing PDFs (extracting, chunking, indexing)…"):
                    raw_text = extract_text_from_pdfs(files)
                    if not raw_text.strip():
                        st.error("No extractable text found in the uploaded PDFs.")
                    else:
                        chunks = split_text(raw_text)
                        vs = build_vectorstore(chunks, api_key)
                        st.session_state.conversation = build_conv_chain(vs, api_key)
                        st.success("Ready! Ask questions in the main panel.")
                        with st.expander("Preview extracted text"):
                            st.text_area("Text", raw_text[:5000], height=250)

prompt = st.chat_input("Ask a question about your documents…")
if prompt:
    if st.session_state.conversation is None:
        st.warning("Please upload and process PDFs first.")
    else:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                resp = st.session_state.conversation({"question": prompt})
            st.session_state.chat_history = resp["chat_history"]
            show_chat([resp["chat_history"][-1]])
