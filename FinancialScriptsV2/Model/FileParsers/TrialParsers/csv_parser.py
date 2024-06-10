import csv
from io import StringIO

class CSVParser:
    @staticmethod
    def load_csv_document(file_content):
        """Load and parse content from a CSV document."""
        # Use StringIO to handle file content as a file-like object
        f = StringIO(file_content.decode('utf-8'))
        reader = csv.reader(f, delimiter=',')
        
        # Extracting text from each row
        rows = [','.join(row) for row in reader]
        text = '\n'.join(rows)
        return text
