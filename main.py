from pdf_loader import load_pdf
from vectorstore import create_vectorstore
from gemini_chain import create_qa_chain
from db import log_interaction

def process_question(pdf_file, question):
    raw_text = load_pdf(pdf_file)
    vectorstore = create_vectorstore(raw_text)
    chain = create_qa_chain(vectorstore)
    answer = chain.run(question)
    log_interaction(question, answer)
    return answer
