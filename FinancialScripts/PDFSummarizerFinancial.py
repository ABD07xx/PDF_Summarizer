# Import necessary libraries and modules
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from Scripts.CustomStuffDocuments import StuffDocumentsChain
from Scripts.config import llm_config

# Define the path to the PDF document
PDF_PATH = "./../PDF/Plaid_Asset_Report.pdf"

# Load the PDF document using PyPDFLoader
def load_pdf_document(path):
    """Load content from a PDF document located at the specified path."""
    loader = PyPDFLoader(path)
    return loader.load()

# Set up the prompt template for processing the document
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

    

