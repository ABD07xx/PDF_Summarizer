import os
import tempfile
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from CustomFiles.CustomStuffDocuments import StuffDocumentsChain
from CustomFiles.config import llm_config


class PDFSummarizer:
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

    @staticmethod
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

    @staticmethod
    def setup_llm_chain(prompt):
        """Set up the language model chain with OpenAI and a given prompt."""
        llm = ChatOpenAI(
            **llm_config
            )
        return LLMChain(llm=llm, prompt=prompt)

    @staticmethod
    def summarize_pdf(file_content):
        """Main function to execute the document summarization process."""
        docs = PDFSummarizer.load_pdf_document(file_content)
        print(docs)
        prompt = PDFSummarizer.create_prompt(docs)
        #print(prompt)
        llm_chain = PDFSummarizer.setup_llm_chain(prompt)
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="docs")
        result = stuff_chain.invoke(docs)
        return result["output_text"]