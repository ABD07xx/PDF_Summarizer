from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
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
def split_text(text, chunk_size=25000):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    return text_splitter.create_documents([text])


# Function to initialize the ChatGPT model
def initialize_llm(config):
    return ChatOpenAI(**config)


# Function to create and run a summarization chain
def run_summarization_chain(llm, chunks, map_prompt=None, combine_prompt=None):
    if map_prompt and combine_prompt:
        map_prompt_template = PromptTemplate(input_variables=["text"], template=map_prompt)
        combine_prompt_template = PromptTemplate(input_variables=["text"], template=combine_prompt)

        summarization_chain = load_summarize_chain(
            llm=llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_template,
            combine_prompt=combine_prompt_template,
            verbose=False
        )
    else:
        summarization_chain = load_summarize_chain(llm, chain_type='map_reduce', verbose=False)

    return summarization_chain.run(chunks)


# Main function to orchestrate the summarization process
def main():
    text = extract_text_from_pdf(PDF_PATH)

    llm = initialize_llm(llm_config)

    chunks = split_text(text)

    # Run the default summarization chain
    default_summary = run_summarization_chain(llm, chunks)
    print("\n\n\n\n\n\n", default_summary)

    # Define custom prompts
    chunks_prompt = "Please summarize the below Document:\nDocument: `{text}`\nSummary:"
    
    final_combine_prompt = """Provide a final summary of the entire Document with these important points.
    Add a Title, Start the summary with an introduction and provide the summary in numbered points for the Document.
    Document: `{text}`"""

    # Run the summarization chain with custom prompts
    custom_summary = run_summarization_chain(
        llm, chunks, map_prompt=chunks_prompt, combine_prompt=final_combine_prompt
    )
    print("\n\n\n\n\n\n")
    print("Custom Prompt Summary:\n", custom_summary)


if __name__ == "__main__":
    main()
