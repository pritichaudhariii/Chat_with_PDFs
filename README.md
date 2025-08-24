**Overview**
------------

The MultiPDF Chat App is an interactive Python application powered by LangChain that lets you converse with multiple PDF files at once. Instead of manually searching through long reports, case studies, or textbooks, you can simply ask questions in plain English — and the app will retrieve relevant information directly from your documents.

**How It Works**
------------
![F657D32A-9E55-42B5-9029-783AC92E5720](https://github.com/user-attachments/assets/be06e763-7791-455b-b122-c25562d854cf)


The app processes your questions through the following workflow:

1. PDF Ingestion: Multiple PDF files are uploaded, and their textual content is extracted.

2. Segmentation: The extracted text is split into smaller, manageable sections for easier handling.

3. Embedding Creation: A language model converts these text sections into vector embeddings that capture their meaning.

4. Relevance Search: When you ask a question, it is also converted into an embedding and compared against the stored text sections to find the closest matches.

5. Answer Construction: The most relevant sections are fed back into the language model, which generates an answer tailored to the information contained in your PDFs.

**Dependencies and Installation**
------------

To install the MultiPDF Chat App, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:

   ```bash
   pip install -r requirements.txt

3. Obtain an API key from OpenAI and add it to the .env file in the project directory.
   
   ```bash
   OPENAI_API_KEY=your_secrit_api_key

**Usage**
------------

To use the MultiPDF Chat App, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

2. Run the `app.py` file using the Streamlit CLI. Execute the following command:

   ```bash
   streamlit run app.py

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple PDF documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded PDFs using the chat interface




