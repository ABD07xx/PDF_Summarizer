<h1>PDF Summarizer</h1>

Overview
-----------------
This project is designed to streamline the process of summarizing PDF documents by employing Large Language Models (LLMs). Specifically, the system is tailored to process financial PDFs, making it particularly useful for extracting insights and identifying trends and finding anamplies and stuff. All of this can be tailored according to the needs. The application functions by reading a PDF document and then passing its content through a chain finally reaching LLMs. Each model in the chain contributes to refining and condensing the information, resulting in a comprehensive yet succinct summary.

One of the key features of this system is its flexibility. The model chain remains consistent across different applications, which means that modifications to the system—such as changing the model or tweaking the prompts—can be made without altering the underlying structure. This ensures that the system can be easily upgraded or adapted to new requirements in the future. The use of LLM chains in this context not only enhances the efficiency of document processing but also offers significant adaptability for continuous improvement and customization according to evolving needs.

Directory Overview
----------------------
    - We have 2 main directories present in this project `DifferentMethods` and `FinancialScripts. Different Methods contains Custom Files and some Python files that we have used to check the different methods that we can employ to summarise the PDFs effectively After thorough testing and overriding some libraries we found that desired outputs. The Files we changed along with the custom files are placed in the CustomFiles folder. 
    - The `FinancialScripts` Directory contains code that is tailored to analyse PDFs regarding Financial Domain. The answers can be further improved by improving the prompts.

Proposed Models
---------------------
    - Sequential Model with PII obfuscation: 
![Sequential](https://drive.google.com/file/d/13dVm2J2kTklIcTi79vgtx4lqAdKWhDll/view?usp=sharing)
        
    - Stuffing with with PII obfuscation
![Stuffing)](https://drive.google.com/file/d/1OKACWN4r-eVl3ewfmhSL0d7mhmQxMK3F/view?usp=sharing)




Installation
-----------------------

### Prerequisites
Ensure you have Python installed on your machine. Python 3.8 or newer is recommended.

Along with Python you should have access to OPENAI API key or for the matter any API Key that you want to use. If you are using LLM models locally then just change the config file according to that. 

Dependencies
---------------------
Install the necessary Python libraries by running the following command in your terminal:

pip install langchain==0.1.20
pip install langchain_community==0.0.38
pip install langchain_core==0.1.52
pip install langchain_openai==0.1.6
pip install presidio_analyzer==2.2.354
pip install presidio_anonymizer==2.2.354
pip install PyPDF2==3.0.1


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


Configurations
---------------------
Configure the language model parameters in the config.py file. This includes API keys and settings related to the OpenAI model used.

Custom Models
-----------------------
This project uses custom classes (Custom_LLMChain, StuffDocumentsChain) for handling specific logic and interactions. These classes encapsulate the details necessary for integrating different components and managing the data flow.

New Functionalities
-------------------------
Custom Language Model Integration: Users now have the flexibility to integrate any LLM, including GPT and Llama3, by modifying the config.py.

Enhanced Summarization Techniques: The application leverages advanced MapReduce techniques for summarizing extensive documents, improving efficiency and scalability.
