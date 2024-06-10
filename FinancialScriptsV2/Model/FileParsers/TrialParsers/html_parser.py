from bs4 import BeautifulSoup

class HTMLParser:
    @staticmethod
    def load_html_document(file_content):
        """Load and parse content from an HTML document."""
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(file_content, 'html.parser')
        text = soup.get_text()
        return text
