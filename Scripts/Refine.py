from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from Scripts.config import llm_config

PDF_PATH = "./../PDF/Bartleby, The Scrivener A Story Of Wall-street Author Herman Melville.pdf"

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    pdfreader = PdfReader(pdf_path)
    return "".join([page.extract_text() for page in pdfreader.pages if page.extract_text()])

# Function to split text into chunks using RecursiveCharacterTextSplitter
def split_text(text, chunk_size=25000):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    return text_splitter.create_documents([text])

# Function to initialize the ChatGPT model
def initialize_llm(config):
    return ChatOpenAI(**config)

# Function to create and run a summarization chain
def run_summarization_chain(llm, chunks):
    summarization_chain = load_summarize_chain(
        llm,
        chain_type='refine',
        verbose=True
    )
    return summarization_chain.run(chunks)

# Main function to orchestrate the summarization process
def main():
    text = extract_text_from_pdf(PDF_PATH)
    llm = initialize_llm(llm_config)
    chunks = split_text(text)
    refined_summary = run_summarization_chain(llm, chunks)
    
    print("Refined Summary: \n", refined_summary)

if __name__ == "__main__":
    main()
