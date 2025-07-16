from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

def create_qa_chain(vectorstore):
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro", temperature=0.2)
    return RetrievalQA.from_chain_type(llm=model, retriever=vectorstore.as_retriever())
