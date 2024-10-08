<h1>PDF Summarizer</h1>

Overview
--------------------------------
This project is designed to streamline the process of summarizing PDF documents by employing Large Language Models (LLMs). Specifically, the system is tailored to process financial PDFs, making it particularly useful for extracting insights and identifying trends and finding anamplies and stuff. All of this can be tailored according to the needs. The application functions by reading a PDF document and then passing its content through a chain finally reaching LLMs. Each model in the chain contributes to refining and condensing the information, resulting in a comprehensive yet succinct summary.

One of the key features of this system is its flexibility. The model chain remains consistent across different applications, which means that modifications to the system—such as changing the model or tweaking the prompts—can be made without altering the underlying structure. This ensures that the system can be easily upgraded or adapted to new requirements in the future. The use of LLM chains in this context not only enhances the efficiency of document processing but also offers significant adaptability for continuous improvement and customization according to evolving needs.

Directory Overview
-----------------------------
We have 2 main directories present in this project `DifferentMethods` and `FinancialScripts. Different Methods contains Custom Files and some Python files that we have used to check the different methods that we can employ to summarise the PDFs effectively After thorough testing and overriding some libraries we found that desired outputs. The Files we changed along with the custom files are placed in the CustomFiles folder. 

The `FinancialScripts` Directory contains code that is tailored to analyse PDFs regarding Financial Domain. The answers can be further improved by improving the prompts.

Proposed Models
----------------------------
    - Sequential Model with PII obfuscation: 
![Sequential](Assets/Sequential.png)
        
    - Stuffing with with PII obfuscation
![Stuffing)](Assets/Stuffing.png)


Installation
-----------------------

### Prerequisites
Ensure you have Python installed on your machine. Python 3.9 or newer is recommended.

Along with Python you should have access to OPENAI API key or for the matter any API Key that you want to use. If you are using LLM models locally then just change the config file according to that. 

Dependencies
---------------------
Install the necessary Python libraries by running the following command in your terminal:

<ul>
  <li>pip install langchain==0.1.20</li>
  <li>pip install langchain_community==0.0.38</li>
  <li>pip install langchain_core==0.1.52</li>
  <li>pip install langchain_openai==0.1.6</li>
  <li>pip install presidio_analyzer==2.2.354</li>
  <li>pip install presidio_anonymizer==2.2.354</li>
  <li>pip install PyPDF2==3.0.1</li>
</ul>


To run the project, follow these steps:
----------------------------------------

Place your target PDF documents in the PDF directory within your project folder.

Open your terminal and navigate to the project directory.

Run the script using the following command:

<b>*python name_of_your_script.py*</b>

Replace name_of_your_script.py with the actual name of your Python script.

Running Local LLM using Ollama
----------------------------------------------
We have used Llama 3

Open Terminal use <b>litellm --model ollama/llama3</b>

If Llama3 isn't installed

Use <b>ollama pull llama3</b>

You can use any of the LLMs even GPT by Open AI just update the config files.


Code Structure
-------------------
<ul>
    <li><strong>Document Loading</strong>:
        <ul>
            <li>Utilizes the <code>PyPDFLoader</code> class from the <code>langchain_community.document_loaders.pdf</code> module to load PDF documents.</li>
        </ul>
    </li>
    <li><strong>Prompt Template</strong>:
        <ul>
            <li>A custom prompt template is created to instruct the language model on how to process the document.</li>
        </ul>
    </li>
    <li><strong>Language Model Configuration</strong>:
        <ul>
            <li>Configures the <code>ChatOpenAI</code> class with necessary parameters (from <code>config.py</code>) to interact with OpenAI's language models.</li>
        </ul>
    </li>
    <li><strong>Model Chain Setup</strong>:
        <ul>
            <li>Integrates the language model with the prompt using the <code>LLMChain</code> class.</li>
            <li>Uses the <code>StuffDocumentsChain</code> to handle the interaction flow and execution based on the document content.</li>
        </ul>
    </li>
    <li><strong>Summarize Using MapReduce</strong>:
        <ul>
            <li>Employs a MapReduce approach to efficiently summarize large documents.</li>
            <li>Splits the document into smaller chunks and uses a large language model to summarize each chunk independently.</li>
            <li>Combines individual summaries into a comprehensive summary, ensuring it captures the essential points of the entire document with added scalability.</li>
        </ul>
    </li>
    <li><strong>Summarize Using Sequential</strong>:
        <ul>
            <li>Utilizes a sequential model to effectively summarize large documents.</li>
            <li>After splitting the document, intermediate summaries of chunks are created and passed along with the chunks to produce a global summary.</li>
            <li>Follows a sequential process.</li>
        </ul>
    </li>
    <li><strong>Summarize Using Refine</strong>:
        <ul>
            <li>Similar to the sequential method with minor changes in the optimality of the algorithm.</li>
        </ul>
    </li>
</ul>


Endpoint Configuration
-------------------------
One Endpoint has also been created. This time its only for `PDFSummarizerFinancial` present in <b>Financial Scripts</b> directory. The endpoint name is `PDFSummarizerFinancialEndpoint`.

To run it simply use <b>`uvicorn PDFSummarizerFinancialEndpoint:app --reload`</b>



Configurations
-------------------------
Configure the language model parameters in the config.py file. This includes API keys and settings related to the OpenAI model used.

Custom Models
----------------------------
This project uses custom classes (Custom_LLMChain, StuffDocumentsChain) for handling specific logic and interactions. These classes encapsulate the details necessary for integrating different components and managing the data flow.

New Functionalities
-------------------------
Custom Language Model Integration: Users now have the flexibility to integrate any LLM, including GPT and Llama3, by modifying the config.py.

Enhanced Summarization Techniques: The application leverages advanced MapReduce techniques for summarizing extensive documents, improving efficiency and scalability


<h1> V2 </h1>


The project introduces a robust and dynamic API service designed to streamline the processing and summarization of financial documents across various formats and types. Leveraging advanced text parsing and language model technologies, the API offers powerful functionalities to handle documents in CSV, JSON, Text, HTML, and PDF formats. It supports a range of financial document types, including credit reports, profit and loss statements, bank statements, and asset summaries. Additionally, the service provides flexibility to handle different loan types, defaulting to 'auto' for simplicity. Users also have the option to supply custom prompts to tailor the summarization process to their specific needs. This integration of diverse functionalities makes the API a comprehensive solution for document management and summarization tasks, facilitating accurate and efficient information extraction and reporting.


<h1>Added Functionalities</h1>

# UniversalParser

## Introduction
The `UniversalParser` is a Python class designed to facilitate the parsing of documents in various formats including CSV, HTML, JSON, PDF, and Text. Each method within the class handles the creation and deletion of temporary files seamlessly, making it easy for users to load and parse content without having to manage file handling explicitly.

## Features
- **Load CSV Documents**: Parse CSV files from binary content.
- **Load HTML Documents**: Parse HTML files from binary content.
- **Load JSON Documents**: Load and parse JSON files using a specified schema.
- **Load PDF Documents**: Parse PDF files from binary content.
- **Load Text Documents**: Parse plain text files from binary content.

# DocumentPromptCreator

## Introduction
`DocumentPromptCreator` is a Python class that serves as a utility for generating structured prompts for language models, specifically tailored for summarizing financial documents. The class uses predefined templates based on the type of financial document (e.g., credit reports, bank statements, asset summaries, and profit and loss statements). It simplifies the process of guiding language models to extract and summarize key financial data accurately and consistently.

## Features
- **Document Type Specific Summaries**: Handles various financial document types including `credit`, `bank`, `asset`, and `profit_loss`. Each type has a customized template that highlights key information relevant to that document type.
- **Customizable Prompt Templates**: In addition to predefined templates, users can specify custom prompts for document types not covered by the default options, providing flexibility in application.
- **Structured Output**: The prompts are structured to guide language models to produce outputs that are not only relevant but also organized in a manner conducive to financial analysis.
- **Ease of Use**: Users can easily generate prompts by providing the document content and specifying the document type. The class handles the creation of detailed, structured prompts based on the input.
- **Scalability and Extensibility**: New document types and templates can be added to the `doc_type_prompts` dictionary, making it easy to scale and extend the class to cover additional types of financial documents.

# Document Processing and Summarization Tool

## Introduction
This tool is designed to streamline the processing and summarization of various types of documents using advanced language model chains from OpenAI. It includes functionality to parse different document formats, generate structured prompts for document summarization, and utilize language models to provide detailed summaries. The tool leverages Python modules and custom configurations for optimal performance in handling complex text-based operations.

## Features
- **Multi-Format Document Parsing**: Supports parsing of multiple document types including CSV, HTML, JSON, PDF, and plain text. This feature uses a unified interface (`UniversalParser`) to handle various file types effectively.
- **Dynamic Prompt Generation**: Capable of generating custom prompts based on the document's content, type, and other parameters such as loan type. This feature allows for flexibility in guiding the summarization process according to specific requirements.
- **Language Model Integration**: Utilizes OpenAI's language models through the `LLMChain` setup, enabling detailed and context-aware summarizations of the document content. The configuration can be customized via `llm_config`.
- **Custom Document Chains**: Incorporates a custom document chain (`StuffDocumentsChain`), designed to handle specific document-related tasks within the language model processing pipeline, enhancing the model's focus on relevant details.
- **Error Handling and Extensibility**: Includes robust error handling for unsupported file types and allows for easy extension to include more document types or custom processing rules.

# FastAPI Document Summarization Service

## Introduction
This FastAPI service is built to offer an API endpoint for uploading and summarizing documents. It utilizes advanced text processing techniques to parse and summarize documents based on their content and type. This service is capable of handling various document formats, making it versatile for different use cases such as financial analysis, asset management, and credit evaluation.

## Features
- **Document Type Support**: Handles multiple document formats including CSV, HTML, JSON, PDF, and plain text. This feature allows the service to be flexible in terms of the input it can process.
- **Dynamic Summarization**: Integrates a sophisticated summarization module (`Summarizer`) which leverages language model chains to generate concise summaries from detailed documents.
- **Custom Prompt Generation**: The service can generate tailored prompts based on the document type and optional parameters (like loan type), ensuring that the summarization is relevant to the specific context of the document.
- **Enumeration for Document Types**: Uses a Python Enum to manage different types of documents, supporting clear and error-free handling of document categorization within the API.
- **Temporary File Handling**: Implements secure and clean temporary file handling to ensure that uploaded documents are stored safely during processing and are cleaned up afterward, preserving server integrity and performance.
- **Built with FastAPI**: Utilizes FastAPI's asynchronous features to efficiently handle file uploads and processing, providing a responsive and scalable server environment.
- **Easy Deployment and Testing**: Includes integration with `uvicorn` for simple local testing and deployment, making it straightforward to get the server running and accessible.

Dependencies
---------------------
Install the necessary Python libraries by running the following command in your terminal:

<ul>
<li>langchain==0.1.20</li>
<li>langchain_community==0.0.38</li>
<li>langchain_core==0.1.52</li>
<li>langchain_openai==0.1.6</li>
<li>presidio_analyzer==2.2.354</li>
<li>presidio_anonymizer==2.2.354</li>
<li>PyPDF2==3.0.1</li>
<li>litellm==1.35.23</li>
<li>ollama==0.1.3</li>
<li>pydantic</li>
<li>IPython</li>
<li>tempfile</li>
<li>fastapi</li>
<li>fastembed</li>
<li>pyyaml</li>
<li>openpyxl</li>
<li>pydantic_settings</li>
<li>uvicorn</li>
<li>enum</li>
<li>jq</li>
</ul>

Endpoint Configuration
-------------------------

To run it simply use <b>`uvicorn PDFSummarizerFinancialV2Endpoint:app --reload`</b>

<b> Note </b>

- Please make it sure you are inside `FinancialScriptsV2` and there inside `Model` `directory` before running this command
- For v2 prompts needs to be adjusted and are just for demo purpose.
- 
