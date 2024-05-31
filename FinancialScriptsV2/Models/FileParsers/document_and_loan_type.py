class DocumentAndLoanTypeMapper:
    # Mapping of user inputs to document types
    document_map = {
        "credit": "Credit Report",
        "bank": "Bank Statement",
        "asset": "Asset Report",
        "profit_loss": "Profit & Loss Statement"
    }

    # Placeholder mapping of user inputs to generic loan types
    loan_map = {
        "personal": "Default Personal Loan Type",
        "home": "Default Home Loan Type",
        "auto": "Default Auto Loan Type",
        "education": "Default Education Loan Type"
    }

    @staticmethod
    def get_document_type(user_input):
        """Retrieve the document type based on user input."""
        # Default to None if the input does not match any key
        return DocumentAndLoanTypeMapper.document_map.get(user_input.lower(), None)
    
    @staticmethod
    def get_loan_type(user_input):
        """Retrieve the loan type based on user input, returning a default type if not specified."""
        # Convert input to lowercase to ensure case-insensitive matching
        return DocumentAndLoanTypeMapper.loan_map.get(user_input.lower(), "Unknown Loan Type")
