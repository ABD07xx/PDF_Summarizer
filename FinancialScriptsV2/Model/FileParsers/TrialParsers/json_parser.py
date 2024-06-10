import json

class JSONParser:
    @staticmethod
    def load_json_document(file_content):
        """Load and parse content from a JSON document."""
        # Decode JSON file content
        data = json.loads(file_content)
        return data
