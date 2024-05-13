<h1>PDF Summarizer</h1>

Overview
-----------------
This project automates the summarization of PDF documents using a Large Language Model (LLM) chain. The application reads a PDF document, processes its content with a chain of models, and outputs a concise summary. This can be used to find insights, trends etc. All of this cna be achieved by just changing and tweaking the prompts. The chains will be completely same even if we want to change the model or prompts. This provide more flexibility for future upgrades.

Installation
-----------------------

### Prerequisites
Ensure you have Python installed on your machine. Python 3.8 or newer is recommended.

Dependencies
---------------------
Install the necessary Python libraries by running the following command in your terminal:

pip install langchain-community 
pip install langchain-core 
pip install langchain-openai
pip install pypdf2

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
Document Loading: The PyPDFLoader class from the langchain_community.document_loaders.pdf module is used to load PDF documents.
Prompt Template: A custom prompt template is created to instruct the language model on how to process the document.
Language Model Configuration: The ChatOpenAI class is configured with necessary parameters (from config.py) to interact with OpenAI's language models.
Model Chain Setup: The LLMChain class integrates the language model with the prompt, while StuffDocumentsChain handles the interaction flow and execution based on the document content.
Summarize Using Map Reduce: This feature involves the utilization of a MapReduce approach to summarize large documents efficiently. The process involves splitting the document into smaller chunks and using a large language model to summarize each chunk independently. Afterward, a final summarization step combines these individual summaries into a comprehensive summary, ensuring it captures the essential points of the entire document with added scalability.
Summarise using Sequential: This feature involves the utilization of a sequential model to summarize large documnets effectively. It's different from map reduce as here after splitting the document we create intermediate summaries of chunks and pass these summaries along with the chunks to produce a global summary. Its more like a sequential process.
Summarise using Refine: Its similar to Sequential there are minor changes in the optimality of the algo.

Configurations
Configure the language model parameters in the config.py file. This includes API keys and settings related to the OpenAI model used.

Custom Models
This project uses custom classes (Custom_LLMChain, StuffDocumentsChain) for handling specific logic and interactions. These classes encapsulate the details necessary for integrating different components and managing the data flow.

New Functionalities
Custom Language Model Integration: Users now have the flexibility to integrate any LLM, including GPT and Llama3, by modifying the config.py.
Enhanced Summarization Techniques: The application leverages advanced MapReduce techniques for summarizing extensive documents, improving efficiency and scalability.