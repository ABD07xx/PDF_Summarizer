
import csv
import json
import os
import tempfile
from io import StringIO
from bs4 import BeautifulSoup
from langchain_community.document_loaders.pdf import PyPDFLoader

class UniversalParser:
    @staticmethod
    def load_csv_document(file_content):
        f = StringIO(file_content.decode('utf-8'))
        reader = csv.reader(f, delimiter=',')
        rows = [','.join(row) for row in reader]
        text = '\n'.join(rows)
        return text

    @staticmethod
    def load_html_document(file_content):
        soup = BeautifulSoup(file_content, 'html.parser')
        text = soup.get_text()
        return text

    @staticmethod
    def load_json_document(file_content):
        data = json.loads(file_content)
        return data

    @staticmethod
    def load_pdf_document(file_content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        loader = PyPDFLoader(tmpfile_path)
        result = loader.load()

        os.unlink(tmpfile_path)
        return result

    @staticmethod
    def load_text_document(file_content):
        text = file_content.decode('utf-8')
        return text
