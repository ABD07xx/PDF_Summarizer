import os
import tempfile
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import RedirectResponse
from enum import Enum
from FinancialSummarizerV2 import Summarizer, parse_document, generate_prompt

# Initialize the FastAPI application
app = FastAPI()

# Define an enumeration for supported document types
class DocumentType(str, Enum):
    credit = 'credit'
    bank = 'bank'
    asset = 'asset'
    profit_loss = 'profit_loss'
    default = 'default'

#Endpoint basic
@app.get("/")  
def welcome():
    return RedirectResponse(url='/docs')



# Define an endpoint to handle document summarization requests
@app.post("/summarize/")
async def summarize_document(file: UploadFile = File(...),
                             doc_type: DocumentType = Form(...),
                             loan_type: str = Form("auto"),
                             prompt: str = Form(None)):
    """
    Endpoint to summarize the content of the uploaded document.
    This function handles file upload, document parsing, prompt generation, and text summarization.
    """
    try:
        # Create a temporary file to store the uploaded document, preserving the original file extension
        suffix = os.path.splitext(file.filename)[1]  # Extract the file extension from the uploaded file name
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file_content = await file.read()  # Read the binary content of the uploaded file
            tmp.write(file_content)
            file_path = tmp.name  # Store the path of the temporary file

        # Verify if the file extension is supported by the parser
        if suffix.lower() in ['.csv', '.html', '.json', '.pdf', '.txt']:
            # Parse the document to extract relevant content based on its type
            parsed_content = parse_document(file_path)
            # Optionally print the parsed content for debugging
            print(parsed_content)
            # Generate a prompt for summarization using the document type, loan type, and custom prompt (if provided)
            prompt = generate_prompt(parsed_content, doc_type.value, loan_type, prompt)
            # Use the summarizer to generate a summary of the document based on the generated prompt
            summary = Summarizer.summarize(parsed_content, prompt)
            # Return the summary in JSON format
            return {"summary": summary}
        else:
            # Raise an error if the file type is not supported
            raise ValueError("Unsupported file type: " + suffix)
    finally:
        # Clean up by deleting the temporary file after processing
        os.unlink(file_path)

# Run the application using Uvicorn if the script is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
