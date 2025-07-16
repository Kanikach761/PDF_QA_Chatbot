import streamlit as st
from main import process_question
import pandas as pd

st.set_page_config(page_title="📄 PDF Q&A with Gemini", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>📄 PDF Question Answering App</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

if "question" not in st.session_state:
    st.session_state.question = ""

def clear_history():
    st.session_state.qa_history = []

def clear_question():
    st.session_state.question = ""

col1, col2 = st.columns([1, 2])

with col1:
    pdf = st.file_uploader("Upload your PDF document", type="pdf", help="Upload a PDF file to ask questions.")

    # Clear history button
    if st.session_state.qa_history:
        if st.button("🧹 Clear Q&A History"):
            clear_history()

with col2:
    if pdf:
        question = st.text_input(
            "Ask a question based on the PDF:",
            value=st.session_state.question,
            key="input_box",
            on_change=clear_question,
            placeholder="Type your question here and press Enter"
        )

        if question:
            with st.spinner("Processing your question..."):
                try:
                    answer = process_question(pdf, question)
                    st.session_state.qa_history.append({"Question": question, "Answer": answer})
                    clear_question()
                except Exception as e:
                    st.error(f"⚠️ Error occurred: {e}")

# Show Q&A history
if st.session_state.qa_history:
    st.markdown("---")
    st.markdown(f"### 📚 Q&A History ({len(st.session_state.qa_history)} questions asked)")

    for i, qa in enumerate(reversed(st.session_state.qa_history)):
        st.markdown(
            f"""
            <div style="background-color:#E0F7FA; padding:10px; border-radius:10px; margin-bottom:5px;">
                <strong style="color:#00796B;">You:</strong> {qa['Question']}
            </div>
            <div style="background-color:#FFF9C4; padding:10px; border-radius:10px 10px 10px 0; margin-bottom:15px;">
                <strong style="color:#F9A825;">Bot:</strong> {qa['Answer']}
            </div>
            """, unsafe_allow_html=True)

    # Download buttons
    df = pd.DataFrame(st.session_state.qa_history)
    txt_output = "\n\n".join([f"Q: {row['Question']}\nA: {row['Answer']}" for row in st.session_state.qa_history])
    txt_bytes = txt_output.encode('utf-8')
    csv = df.to_csv(index=False).encode('utf-8')

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button("⬇️ Download as TXT", txt_bytes, file_name="qa_history.txt")
    with col_dl2:
        st.download_button("⬇️ Download as CSV", csv, file_name="qa_history.csv")
else:
    st.info("Upload a PDF and ask questions to get started!")
