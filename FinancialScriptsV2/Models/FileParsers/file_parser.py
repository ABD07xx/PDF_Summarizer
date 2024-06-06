import os
import tempfile
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.html import UnstructuredHTMLLoader

class UniversalParser:
    """
    A universal parser class that provides static methods to load documents of different types,
    such as CSV, HTML, JSON, PDF, and Text. Each method reads from a temporary file,
    processes it with the appropriate loader, and deletes the temporary file after loading.
    """

    @staticmethod
    def load_csv_document(file_content):
        """
        Loads a CSV document from the provided binary content.

        Args:
        file_content (bytes): Binary content of the CSV file.

        Returns:
        object: Parsed data from the CSV file.
        """
        # Create a temporary file with the CSV content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        # Load the CSV file using a CSV loader
        loader = CSVLoader(tmpfile_path)
        result = loader.load()

        # Delete the temporary file
        os.unlink(tmpfile_path)
        return result

    @staticmethod
    def load_html_document(file_content):
        """
        Loads an HTML document from the provided binary content.

        Args:
        file_content (bytes): Binary content of the HTML file.

        Returns:
        object: Parsed data from the HTML file.
        """
        # Create a temporary file with the HTML content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        # Load the HTML file using an unstructured HTML loader
        loader = UnstructuredHTMLLoader(tmpfile_path)
        result = loader.load()

        # Delete the temporary file
        os.unlink(tmpfile_path)
        return result

    @staticmethod
    def load_json_document(file_content):
        """
        Loads a JSON document directly from a path to a file containing JSON data.

        Args:
        file_content (str): Path to the JSON file.

        Returns:
        object: Parsed data from the JSON file.
        """
        # Load JSON data using a JSON loader with specified jq_schema
        loader = JSONLoader(
            file_path=file_content,
            jq_schema='.',
            text_content=False
        )
        data = loader.load()
        return data

    @staticmethod
    def load_pdf_document(file_content):
        """
        Loads a PDF document from the provided binary content.

        Args:
        file_content (bytes): Binary content of the PDF file.

        Returns:
        object: Parsed data from the PDF file.
        """
        # Create a temporary file with the PDF content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        # Load the PDF file using a PDF loader
        loader = PyPDFLoader(tmpfile_path)
        result = loader.load()

        # Delete the temporary file
        os.unlink(tmpfile_path)
        return result

    @staticmethod
    def load_text_document(file_content):
        """
        Loads a text document from the provided binary content.

        Args:
        file_content (bytes): Binary content of the text file.

        Returns:
        object: Parsed data from the text file.
        """
        # Create a temporary file with the text content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmpfile:
            tmpfile.write(file_content)
            tmpfile_path = tmpfile.name

        # Load the text file using a text loader
        loader = TextLoader(tmpfile_path)
        result = loader.load()

        # Delete the temporary file
        os.unlink(tmpfile_path)
        return result
