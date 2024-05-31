from fastapi import FastAPI, File, UploadFile, Form
from enum import Enum
import os
import tempfile

from FinancialSummarizerV2 import Summarizer, parse_document, generate_prompt, get_document_and_loan_details

app = FastAPI()

class DocumentType(str, Enum):
    credit = 'credit'
    bank = 'bank'
    asset = 'asset'
    profit_loss = 'profit_loss'
    default = 'default'

@app.post("/summarize/")
async def summarize_document(file: UploadFile = File(...),
                             doc_type: DocumentType = Form(...),
                             loan_type: str = Form("auto"),
                             prompt: str = Form(None)):
    """
    Endpoint to summarize the content of the uploaded document.
    """
    try:
        # Create a temporary file to store the uploaded content and preserve the original file extension
        suffix = os.path.splitext(file.filename)[1]  # Extract the extension from the uploaded file name
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            file_content = await file.read()  # Read the file content
            tmp.write(file_content)
            file_path = tmp.name  # Temporary file path with the original file extension
            print("File path:", file_path)

        # Check if the file extension is supported
        if suffix.lower() in ['.csv', '.html', '.json', '.pdf', '.txt']:
            # Read and parse document content
            parsed_content = parse_document(file_path)
            # Get document and loan details
            #document_details, loan_details = get_document_and_loan_details(doc_type.value, loan_type)
            #print(doc_type.value,"\n",loan_details)
            # Generate prompt based on the document content and details
            generated_prompt = generate_prompt(doc_content=parsed_content, doc_type=doc_type.value, loan_type=loan_type, custom_prompt=prompt)

            # Summarize the document content using the generated prompt
            summary = Summarizer.summarize(parsed_content,generated_prompt)
            return {"summary": summary}
        else:
            raise ValueError("Unsupported file type: " + suffix)
    finally:
        # Ensure the temporary file is deleted after processing
        os.unlink(file_path)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
