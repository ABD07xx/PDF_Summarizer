from langchain_core.prompts import PromptTemplate

class DocumentPromptCreator:
    # Map each document type to its specific and default prompt sections
    doc_type_prompts = {
        "credit": """
        Credit Score:
        - Mention the current credit score and any factors influencing changes in the score.

        Outstanding Debts:
        - List all debts, including credit card debts, mortgages, and other loans, with respective amounts and payment statuses.

        Payment History:
        - Detail the payment consistency, highlighting any late payments and their resolutions.

        Financial Delinquencies:
        - Note any instances of financial delinquencies and measures taken to resolve them.

        Overall Creditworthiness:
        - Assess the individual's financial stability and ability to manage and repay debts.
        """,


        "bank": """
        Account Summary:
        - List each type of account (e.g., checking, savings) along with the current balances and any notable changes.

        Transaction Overview:
        - Summarize key transactions, including deposits, withdrawals, and transfers, with dates and amounts.

        High-Value Transactions:
        - Identify any large transactions that significantly affect the account balance.

        Recurring Payments and Deposits:
        - Outline regular incoming and outgoing payments.

        Financial Insights:
        - Offer insights into the financial behavior indicated by the transactions, such as saving patterns, frequent expenses, or potential overdraft risks.
        """,



        "asset": """
        Asset Details:
        - Describe each asset, including real estate, vehicles, investments, and other significant assets.

        Valuation:
        - Detail the current market value of each asset and any recent changes in valuation.

        Asset Liquidity:
        - Assess the liquidity of the assets and their potential to be quickly converted into cash.

        Collateral Potential:
        - Evaluate the suitability of the assets as collateral for the loan.

        Financial Position:
        - Summarize the overall financial position based on the asset holdings.
        """,



        "profit_loss": """
        Revenue Analysis:
        - Break down the revenue sources and compare them to previous periods.

        Expense Review:
        - Itemize expenses by category and discuss any significant or unusual expenditures.

        Net Income:
        - Calculate and discuss the net income, noting trends and factors affecting profitability.

        Financial Health:
        - Evaluate the financial health of the business, considering the ability to sustain operations and repay debts.

        Future Projections:
        - Offer insights into potential future earnings based on current financial trends.
        """,



        "default": """
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
        """
    }

    @staticmethod
    def create_prompt(docs, doc_type):
        """
        Create a prompt template for the language model to summarize the document based on the document type or a user-defined input.

        Args:
            docs (str): The document content for the prompt.
            doc_type (str): The type of document which determines the prompt template used, or 'custom' for user-defined prompts.

        Returns:
            PromptTemplate: A PromptTemplate object containing the formatted prompt.
        """
        # Handle empty or whitespace-only input by returning the default prompt
        #if not docs.strip():
            #return PromptTemplate.from_template(DocumentPromptCreator.doc_type_prompts["default"])

        # Fetch the specific section from the map; use a default section if doc_type is unrecognized
        doc_specific_section = DocumentPromptCreator.doc_type_prompts.get(doc_type, DocumentPromptCreator.doc_type_prompts["default"])

        prompt_template = """
            A PDF document containing financial transactions is provided:
            Document:
            "{docs}"

            Please read through the document carefully. Inside <scratchpad> tags, write out your initial thoughts on how you will approach summarizing the financial information in the document. Consider what key details to extract and how you will organize the summary.

            Now, please provide a detailed financial summary of the transactions in the document, focusing on the following sections:
            """ 

        # Append the f-string part with 'doc_specific_section'
        prompt_template += f"""{doc_specific_section}
        Please provide your final financial summary inside <financial_summary> tags.
        Summary:
        """
        return PromptTemplate.from_template(prompt_template)

# Usage example:
# Create an instance and call the method with document content and type
# prompt_instance = DocumentPromptCreator.create_prompt("Document text goes here...", "credit")
