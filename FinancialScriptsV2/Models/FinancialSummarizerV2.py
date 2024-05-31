import os
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from CustomFiles.CustomStuffDocuments import StuffDocumentsChain
from CustomFiles.config import llm_config
from FileParsers.file_parser import UniversalParser
from FileParsers.document_and_loan_type import DocumentAndLoanTypeMapper
from Prompts.Prompts import DocumentPromptCreator

# Mapping file extensions to their respective parser functions
file_parsers = {
    '.csv': UniversalParser.load_csv_document,
    '.html': UniversalParser.load_html_document,
    '.json': UniversalParser.load_json_document,
    '.pdf': UniversalParser.load_pdf_document,
    '.txt': UniversalParser.load_text_document
}

def parse_document(file_path):
    """Determine the parser based on file extension and parse the document."""
    print("File path:", file_path)
    _, file_extension = os.path.splitext(file_path)
    print("File extension:", file_extension)
    file_extension = file_extension.lower()

    if file_extension in file_parsers:
        with open(file_path, 'rb') as file:
            file_content = file.read()
        return file_parsers[file_extension](file_content)
    else:
        raise ValueError("Unsupported file type: " + file_extension)



def get_document_and_loan_details(doc_type, loan_type="auto"):
    document_details = DocumentAndLoanTypeMapper.get_document_type(doc_type)
    loan_details = DocumentAndLoanTypeMapper.get_loan_type(loan_type)
    return document_details, loan_details




def generate_prompt(doc_content, doc_type, loan_type="auto", custom_prompt=None):
    """
    Generate the appropriate prompt based on document type, loan type, and optionally a custom prompt.
    
    Parameters:
    - doc_content (str): The content of the document.
    - doc_type (str): The type of the document, e.g., 'mortgage', 'lease agreement'.
    - loan_type (str): The type of loan, defaults to 'auto'.
    - custom_prompt (str, optional): A custom prompt provided by the user.

    Returns:
    - str: A generated prompt based on the provided parameters or the custom prompt if provided.
    """
    if custom_prompt:
        return f"""The document is {doc_content} and you have to {custom_prompt}"""  # Use the custom prompt if provided
    
    try:
        # Attempt to generate a prompt using the DocumentPromptCreator class
        return DocumentPromptCreator.create_prompt(doc_content, doc_type)
    except Exception as e:
        # Log or handle the exception appropriately
        raise ValueError(f"Failed to generate prompt: {e}")

class Summarizer:
    @staticmethod
    def setup_llm_chain(prompt):
        """Set up the language model chain with OpenAI and a given prompt."""
        llm = ChatOpenAI(
            **llm_config
            )
        return LLMChain(llm=llm, prompt=prompt)

    @staticmethod
    def summarize(content, prompt_text):
        """Use the language model chain to summarize the document content."""
        llm_chain = Summarizer.setup_llm_chain(prompt_text)
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name='docs')
        result = stuff_chain.invoke(content)
        return result["output_text"]
