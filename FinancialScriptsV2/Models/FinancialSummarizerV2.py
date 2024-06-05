import os
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from CustomFiles.CustomStuffDocuments import StuffDocumentsChain
from CustomFiles.config import llm_config
from FileParsers.file_parser import UniversalParser
from FileParsers.document_and_loan_type import DocumentAndLoanTypeMapper
from Prompts.Prompts import DocumentPromptCreator
from langchain_core.prompts import PromptTemplate
import tempfile
from langchain_community.document_loaders.pdf import PyPDFLoader

# Mapping file extensions to their respective parser functions
file_parsers = {
    '.csv': UniversalParser.load_csv_document,
    '.html': UniversalParser.load_html_document,
    '.json': UniversalParser.load_json_document,
    '.pdf': UniversalParser.load_pdf_document,
    '.txt': UniversalParser.load_text_document
}
@staticmethod
def load_pdf_document(file_content):
    """Load content from a PDF document using a temporary file."""
    # Create a temporary file to write the PDF content
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
        tmpfile.write(file_content)
        tmpfile_path = tmpfile.name

    # Load the PDF using the temporary file path
    loader = PyPDFLoader(tmpfile_path)
    result = loader.load()

    # Clean up the temporary file
    os.unlink(tmpfile_path)
    
    return result

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

def create_prompt(docs):
    """Create a prompt template for the language model to summarize the document."""
    prompt_template = """
        A PDF document containing financial transactions is provided:
        Document:
        "{docs}"

        Please read through the document carefully. Inside <scratchpad> tags, write out your initial thoughts on how you will approach summarizing the financial information in the document. Consider what key details to extract and how you will organize the summary.

        Now, please provide a detailed financial summary of the transactions in the document, focusing on the following sections:

        Summary of Account Balances:
        - List each account mentioned along with its current balance and account type (e.g., Checking, Savings, Credit, Investment).

        Transaction Details:
        - For each account, summarize the transactions including:
        - Dates of transactions
        - Descriptions of each transaction (e.g., salary payment, automatic payments, refunds)
        - Amounts credited and debited
        - Final daily balance after each transaction

        High-Value Transactions:
        - Highlight any high-value transactions that significantly impact account balances, specifying the transaction amount and date.

        Interest and Fees:
        - Note any interest payments or fees applied to the accounts, specifying the amounts and dates.

        Overall Financial Insights:
        - Provide a summary of the financial health indicated by the transactions, such as:
        - Total amount credited vs. debited
        - Trends in spending or saving
        - Any potential financial issues like overdrafts or high credit utilization

        Pending Transactions:
        - Mention any pending transactions, including their potential impact on account balances.

        Make sure to organize the summary by account, highlighting key insights that reflect the financial activity within the report period. Aim to be concise while capturing the essential details.

        Please provide your final financial summary inside <financial_summary> tags.

    Summary:
    """
    return PromptTemplate.from_template(prompt_template)


def generate_prompt(docs, doc_type, loan_type="auto", custom_prompt=None):
    """
    Generate the appropriate prompt based on document type, loan type, and optionally a custom prompt.
    
    Parameters:
    - docs (str): The content of the document.
    - doc_type (str): The type of the document, e.g., 'mortgage', 'lease agreement'.
    - loan_type (str): The type of loan, defaults to 'auto'.
    - custom_prompt (str, optional): A custom prompt provided by the user.

    Returns:
    - str: A generated prompt based on the provided parameters or the custom prompt if provided.
    """
    if custom_prompt:
        prompt_template = """
            A document will be provided to you
            Document: 
            "{docs}" 
            Using this Document you have to perform actions based on the prompt"""
        prompt_template+=f"""
            Prompt: "{custom_prompt}"
        """
        return PromptTemplate.from_template(prompt_template)  # Use the custom prompt if provided
    else:
        try:
            # Attempt to generate a prompt using the DocumentPromptCreator class
            return DocumentPromptCreator.create_prompt(docs, doc_type)
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
    def summarize(docs,prompt):
        """Use the language model chain to summarize the document content."""   
        llm_chain = Summarizer.setup_llm_chain(prompt)
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="docs")
        result = stuff_chain.invoke(docs)
        return result["output_text"]
