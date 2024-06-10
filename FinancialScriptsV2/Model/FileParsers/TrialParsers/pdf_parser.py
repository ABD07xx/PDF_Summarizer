import tempfile
import os
from PyPDF2 import PdfReader

class PDFParser:
    @staticmethod
    def load_pdf_document(file_content):
        """Load content from a PDF document using a temporary file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        reader = PdfReader(tmpfile_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + ' '

        os.unlink(tmpfile_path)
        
        return text
