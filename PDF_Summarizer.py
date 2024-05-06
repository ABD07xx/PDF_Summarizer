# Import necessary libraries and modules
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from Custom_LLMChain import LLMChain
from CustomStuffDocuments import StuffDocumentsChain
from config import llm_config

# Define the path to the PDF document
PDF_PATH = "./PDF/Bartleby, The Scrivener A Story Of Wall-street Author Herman Melville.pdf"

# Load the PDF document using PyPDFLoader
def load_pdf_document(path):
    """Load content from a PDF document located at the specified path."""
    loader = PyPDFLoader(path)
    return loader.load()

# Set up the prompt template for processing the document
def create_prompt(docs):
    """Create a prompt template for the language model to summarize the document."""
    prompt_template = """
    Write a summary of the following document. By reading the summary user should be able to get an idea of the document
    Only include information that is part of the document. 
    Do not include your own opinion or analysis.
    
    Document:
    "{docs}"
    Summary:
    """
    return PromptTemplate.from_template(prompt_template)

# Configure and instantiate the language model chain
def setup_llm_chain(prompt):
    """Set up the language model chain with OpenAI and a given prompt."""
    llm = ChatOpenAI(
        **llm_config
        )
    return LLMChain(llm=llm, prompt=prompt)

# Main execution function
def main():
    """Main function to execute the document summarization process."""
    docs = load_pdf_document(PDF_PATH)
    prompt = create_prompt(docs)
    llm_chain = setup_llm_chain(prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="docs")
    result = stuff_chain.invoke(docs)
    print(result["output_text"])

if __name__ == "__main__":
    main()

    

