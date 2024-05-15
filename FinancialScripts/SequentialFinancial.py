from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from Scripts.config import llm_config

PDF_PATH = "./../PDF/Plaid_Asset_Report.pdf"

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    pdfreader = PdfReader(pdf_path)
    return "".join([page.extract_text() for page in pdfreader.pages if page.extract_text()])

# Function to split text into chunks using RecursiveCharacterTextSplitter
def split_text(text, chunk_size=5000,chunk_overlap=500):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    return text_splitter.create_documents([text])

# Function to initialize the ChatGPT model
def initialize_llm(config):
    return ChatOpenAI(**config)

# Function to run the custom sequential model for summarization
def run_custom_sequential_model(llm, chunks):
    final_context = ""
    for i in range(len(chunks)):
        local_context = ""
        prompt1 = f"""
            A PDF document containing financial transactions is provided:
            Document:
            "{chunks[i]}"

            Please read through the document carefully. Inside <scratchpad> tags, write out your initial thoughts on how you will approach summarizing the financial information in the document. Consider what key details to extract and how you will organize the summary.
            
            Now, please provide a detailed financial summary of the transactions in the document, focusing on the following sections:

            Summary of Account Balances:
            - List each account mentioned along with its current balance and account type (e.g., Checking, Savings, Credit, Investment).

            Transaction Details(most important):
            - For each account, summarize the transactions including:
                - Dates of transactions
                - Descriptions of each transaction (e.g., salary payment, automatic payments, refunds)
                - Amounts credited and debited. Credited and Debited can be written in the document in various forms, like credit can be written as inflow and debit can be written as outflow
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

            Similar Transactions:
            - These should include recurrent transactions that happen on particular dates. Example can be salary credited on 1 of every month or Loan Deducted on every 10th of month. These transactions if available should also be written in answer.
            Make sure to organize the summary by account, highlighting key insights that reflect the financial activity within the report period. Aim to be concise while capturing the essential details.

            Please provide your final financial summary inside <financial_summary> tags.

            Summary:
            """

        summary = llm.invoke(prompt1)
        local_context += list(summary)[0][1]
    final_context = local_context
    prompt2 = f"""Your job is to produce a final summary.
    We have provided an existing summary up to a certain point: {final_context}
    If the context isn't useful, return the original summary."""

    summary_final = llm.invoke(prompt2)
    return summary_final

# Main function to orchestrate the summarization process
def main():
    text = extract_text_from_pdf(PDF_PATH)
    llm = initialize_llm(llm_config)
    chunks = split_text(text)
    sequential_summary = run_custom_sequential_model(llm, chunks)
    print("Sequential Summary:\n", list(sequential_summary)[0][1])

if __name__ == "__main__":
    main()
