from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from CustomFiles.config import llm_config


PDF_PATH = "./../PDF/Plaid_Asset_Report.pdf"


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    pdfreader = PdfReader(pdf_path)
    return "".join([page.extract_text() for page in pdfreader.pages if page.extract_text()])


# Function to split text into chunks using RecursiveCharacterTextSplitter
def split_text(text, chunk_size=25000):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
    return text_splitter.create_documents([text])

def Presidio(text):

    # Initialize Presidio
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    # Analyze text to find personal information
    analysis_results = analyzer.analyze(text=text, entities=["PERSON", "PHONE_NUMBER", "LOCATION", "EMAIL_ADDRESS", "IBAN"], language='en')

    # Anonymize the findings in the text
    anonymized_results = anonymizer.anonymize(text=text, analyzer_results=analysis_results)

    return anonymized_results.text

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
    text1 = extract_text_from_pdf(PDF_PATH)
    text = Presidio(text1)
    llm = initialize_llm(llm_config)

    chunks = split_text(text)

    # Run the default summarization chain
    default_summary = run_summarization_chain(llm, chunks)
    print("\n\n\n\n\n\n", default_summary)

    # Define custom prompts
    chunks_prompt = """
            A PDF document containing financial transactions is provided:
            Document:
            `{text}`

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
    
    #final_combine_prompt = """Your job is to produce a final summary.
    #We have provided an existing summary up to a certain point:
    #If the context isn't useful, return the original summary `{text}`"""

    # Run the summarization chain with custom prompts
    custom_summary = run_summarization_chain(
        llm, chunks, map_prompt=chunks_prompt, combine_prompt=chunks_prompt
    )
    print("\n\n\n\n\n\n")
    print("Custom Prompt Summary:\n", custom_summary)


if __name__ == "__main__":
    main()
