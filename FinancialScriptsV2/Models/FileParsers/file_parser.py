
import csv
import json
import os
import tempfile
from io import StringIO
from bs4 import BeautifulSoup
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.html import UnstructuredHTMLLoader

class UniversalParser:
    @staticmethod
    def load_csv_document(file_content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        loader = CSVLoader(tmpfile_path)
        result = loader.load()

        os.unlink(tmpfile_path)
        return result

    @staticmethod
    def load_html_document(file_content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        loader = UnstructuredHTMLLoader(tmpfile_path)
        result = loader.load()

        os.unlink(tmpfile_path)
        return result

    @staticmethod
    def load_json_document(file_content):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        loader = JSONLoader(tmpfile_path)
        result = loader.load()

        os.unlink(tmpfile_path)
        return result

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
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        loader = PyPDFLoader(tmpfile_path)
        result = loader.load()

        os.unlink(tmpfile_path)
        return result
