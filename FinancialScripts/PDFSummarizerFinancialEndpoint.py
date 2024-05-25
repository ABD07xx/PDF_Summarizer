# PDFSummarizerFinancialEndpoint.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PDFSummarizerFinancial import PDFSummarizer

app = FastAPI()

@app.post("/summarize/")
async def summarize_pdf_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF.")
    
    try:
        file_content = await file.read()
        summary = PDFSummarizer.summarize_pdf(file_content)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
