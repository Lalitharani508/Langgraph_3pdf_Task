import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_PATH = "db/chroma"
DATA_PATH = "Data"

#--------load and split the documents--------
def load_documents():
    docs = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            docs.extend(loader.load())
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)


#--------vector database--------
def get_vectorstore():
    embedding = OpenAIEmbeddings()

    if os.path.exists(DB_PATH):
        return Chroma(persist_directory=DB_PATH, embedding_function=embedding)

    docs = load_documents()
    chunks = split_documents(docs)

    vectordb = Chroma.from_documents(
        chunks,
        embedding,
        persist_directory=DB_PATH
    )
    return vectordb

#--------nodes--------
def retrieve_nodes(state):
    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    docs = retriever.invoke(state["question"])
    context = "\n".join([doc.page_content for doc in docs])

    return {"context": context}


def generate_answer_nodes(state):
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt = f"""
    Answer the question using the context below.

    Context:
    {state['context']}

    Question:
    {state['question']}
    """

    response = llm.invoke(prompt)

    return {"answer": response.content}