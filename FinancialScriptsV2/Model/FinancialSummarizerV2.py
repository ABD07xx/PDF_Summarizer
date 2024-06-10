import os
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from CustomFiles.CustomStuffDocuments import StuffDocumentsChain
from CustomFiles.config import llm_config
from FileParsers.file_parser import UniversalParser
from Prompts.Prompts import DocumentPromptCreator

# Mapping file extensions to their respective parser functions for various document types
file_parsers = {
    '.csv': UniversalParser.load_csv_document,
    '.html': UniversalParser.load_html_document,
    '.json': UniversalParser.load_json_document,
    '.pdf': UniversalParser.load_pdf_document,
    '.txt': UniversalParser.load_text_document
}


def parse_document(file_path):
    """
    Determine the appropriate parser based on the file extension and parse the document.
    This method supports multiple file types and raises an error if the file type is unsupported.
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension in file_parsers:
        with open(file_path, 'rb') as file:
            file_content = file.read()
        return file_parsers[file_extension](file_content)
    else:
        raise ValueError("Unsupported file type: " + file_extension)

def generate_prompt(docs, doc_type, loan_type="auto", custom_prompt=None):
    """
    Generate a prompt based on document content, document type, and loan type, or use a custom prompt if provided.
    This function allows for flexibility in prompt creation based on user input or predefined settings.
    """
    if custom_prompt:
        prompt_template = """
            This is the document: {docs} and you have to 
        """
        prompt_template+= f"""{custom_prompt}"""
        return PromptTemplate.from_template(prompt_template)  # Use the custom prompt if provided
    else:
        try:
            # Attempt to generate a prompt using the DocumentPromptCreator class
            return DocumentPromptCreator.create_prompt(docs, doc_type)
        except Exception as e:
            # Log or handle the exception appropriately
            raise ValueError(f"Failed to generate prompt: {e}")

class Summarizer:
    @staticmethod
    def setup_llm_chain(prompt):
        """
        Set up a language model chain using OpenAI's API with the specified prompt.
        This setup includes configuring the chain with necessary parameters from `llm_config`.
        """
        llm = ChatOpenAI(**llm_config)
        return LLMChain(llm=llm, prompt=prompt)

    @staticmethod
    def summarize(docs, prompt):
        """
        Summarize the document content using a language model chain.
        This method orchestrates the summarization process by setting up the chain and processing the document.
        """
        llm_chain = Summarizer.setup_llm_chain(prompt)
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="docs")
        result = stuff_chain.invoke(docs)
        return result["output_text"]
