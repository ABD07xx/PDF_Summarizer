from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from config import llm_config

PDF_PATH = "./PDF/Bartleby, The Scrivener A Story Of Wall-street Author Herman Melville.pdf"


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    pdfreader = PdfReader(pdf_path)
    return "".join([page.extract_text() for page in pdfreader.pages if page.extract_text()])


# Function to split text into chunks using RecursiveCharacterTextSplitter
def  split_text(text, chunk_size=25000):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    return text_splitter.create_documents([text])


# Function to initialize the ChatGPT model
def initialize_llm(config):
    return ChatOpenAI(**config)


def run_custom_sequential_model(llm,chunks):
    final_context = ""
    for i in range(len(chunks)):
        local_context = ""
        prompt1 = f"""
        An helpful summarizer. You'll receive a chunk of text and you have to summarize it. During summarization You can take context from summaries of previous chunks.
        If no previous summary is given proceed with providing summary of current. Piece of Chunk is {chunks[i]} and previous context is {local_context}. The summary you produce should be able to
        encapsulate both the previous summary and the summary of the new chunk provided
        """
        summary = llm.invoke(prompt1)
        local_context += (list(summary)[0][1])
        #print(f"For loop {i} I have generated a new prompt")
    final_context = local_context
    prompt2 = f"""You will receive a document.Your task is to provide a concise summary of the text, focusing on the key points, important facts, or significant findings.
    Ensure that the summary is clear, coherent, and flows logically. Organize the main points in a structured manner, aiming to capture the essence of the document
    without delving into unnecessary details. If there are multiple sections or chunks, summarize each section separately and combine them into a cohesive overall summary.
    Keep the summary brief and to the point. 
    Document: {final_context}"""

    summary_final = llm.invoke(prompt2)
    return summary_final

# Main function to orchestrate the summarization process
def main():
    text = extract_text_from_pdf(PDF_PATH)

    llm = initialize_llm(llm_config)

    chunks = split_text(text)

    sequential_sumamry = run_custom_sequential_model(
        llm, chunks
    )

    print("Sequential Summary:\n", list(sequential_sumamry)[0][1])

if __name__ == "__main__":
    main()
