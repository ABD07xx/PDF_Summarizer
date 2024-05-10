# Import necessary modules for summarization and text processing
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from config import llm_config

# Specify the path to the PDF file to be summarized
PDF_PATH = "./PDF/Bartleby, The Scrivener A Story Of Wall-street Author Herman Melville.pdf"

# Initialize a PdfReader instance to load and read the PDF file
pdfreader = PdfReader(PDF_PATH)

# Initialize an empty string to collect the extracted text
text = ""
# Iterate through each page of the PDF, extracting text and concatenating it
for page in pdfreader.pages:
    content = page.extract_text()  # Extract the text from the current page
    if content:  # If text is extracted, add it to the overall text
        text += content

# Initialize the Language Model with the desired configuration
llm = ChatOpenAI(**llm_config)

# Split the extracted text into smaller, manageable chunks
# The RecursiveCharacterTextSplitter divides the text into chunks of the specified size
text_splitter = RecursiveCharacterTextSplitter(chunk_size=25000)
# Create a list of documents containing these chunks
chunks = text_splitter.create_documents([text])

# Load a pre-defined MapReduce chain for summarization
# The map-reduce chain generates summaries using a two-step approach
map_reduce_chain = load_summarize_chain(
    llm,  # Use the initialized Language Model
    chain_type='map_reduce',  # Specify the summarization approach
    verbose=False  # Disable verbose output
)

# Run the map-reduce chain to summarize the chunks
summary = map_reduce_chain.run(chunks)

# Output the summary generated using the default prompts
print("\n\n\n\n\n\n", summary)

# Define a custom prompt to be used for mapping each document chunk
chunks_prompt = """
Please summarize the below Document:
Document: `{text}`
Summary:
"""
# Create a template for this prompt, using the 'text' variable for substitution
map_prompt_template = PromptTemplate(input_variables=["text"], template=chunks_prompt)

# Define a custom prompt for the final summary of the entire document
final_combine_prompt = '''
Provide a final summary of the entire Document with these important points.
Add a Title,
Start the summary with an introduction and provide the summary in numbered points for the Document.
Document: `{text}`
'''
# Create a template for the final prompt, using the 'text' variable for substitution
final_combine_prompt_template = PromptTemplate(input_variables=["text"], template=final_combine_prompt)

# Load a new MapReduce summarization chain using the custom prompts
# The map_prompt is used for mapping each chunk
# The combine_prompt is used to create the final summary
custom_summary_chain = load_summarize_chain(
    llm=llm,  # Use the same Language Model
    chain_type="map_reduce",  # Specify the map-reduce approach
    map_prompt=map_prompt_template,  # Custom mapping prompt
    combine_prompt=final_combine_prompt_template,  # Custom combining prompt
    verbose=False  # Disable verbose output
)

# Run the custom summarization chain to generate the summary
custom_output = custom_summary_chain.run(chunks)

# Output the summary generated using the custom prompts
print("\n\n\n\n\n\n")
print("Custom Prompt Summary:\n", custom_output)
