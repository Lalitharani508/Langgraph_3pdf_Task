import streamlit as st
from Rag_app import get_answer
st.set_page_config(page_title="LangGraph rag Chatbot using multiple documents", page_icon=":robot_face:")
st.title("LangGraph rag Chatbot using multiple documents")
st.write("This is a chatbot that uses multiple documents to answer questions.")

query = st.text_input("Enter your query")
if st.button("Get answer"):
    if query:
        with st.spinner("Thinking..."):
            answer = get_answer(query)
            st.success(answer)