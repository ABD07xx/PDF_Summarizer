class TextParser:
    @staticmethod
    def load_text_document(file_content):
        """Load and parse content from a text file."""
        # Assuming the file_content is a byte stream
        text = file_content.decode('utf-8')
        return text
