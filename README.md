# MedChatBot 

Demo on [Hugging Face Spaces](https://huggingface.co/spaces/tmt3103/MedChatBot).

A medical chatbot application that uses RAG (Retrieval-Augmented Generation) architecture to answer medical questions based on medical literature. The system combines **Google Gemini 2.0 Flash Lite** as the language model with **Pinecone** vector database for efficient document retrieval.

## Technology Stack

- **Backend**: Flask
- **Language Model**: gemini-2.0-flash-lite
- **Vector Database**: Pinecone
- **Embeddings**: HuggingFace sentence-transformers (all-MiniLM-L6-v2)
- **Document Processing**: LangChain, PyPDF
- **Frontend**: HTML/CSS/JavaScript

## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/TMTien31/MedChatBot.git
cd MedChatBot
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get API Keys

#### Google Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the generated key

#### Pinecone API Key:
1. Sign up at [Pinecone](https://www.pinecone.io/)
2. Go to your dashboard
3. Copy your API key from the "API Keys" section

### Step 5: Create Environment File
Create a `.env` file in the project root directory:
```bash
# Create .env file
touch .env  # On macOS/Linux
# or create manually on Windows
```

Add your API keys to the `.env` file:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 6: Prepare Medical Documents
- Place your PDF medical documents in the `Data/` folder
- The project includes "Gale Encyclopedia of Medicine Vol. 1 (A-B).pdf" by default
- You can add more medical PDFs to expand the knowledge base

### Step 7: Create Vector Index (Run Once)
**Important**: This step only needs to be run once initially, or whenever you add new documents to the `Data/` folder.

```bash
python store_index.py
```

This script will:
- Read all PDF files from the `Data/` directory
- Split text into 500-character chunks with 20-character overlap
- Generate embeddings using sentence-transformers
- Create and populate a Pinecone index named "medchatbot"

**Note**: This process may take several minutes depending on the size of your documents.

## Running the Application

### Start the Flask Server
```bash
python app.py
```

### Access the Application
1. Open your web browser
2. Navigate to: `http://0.0.0.0:8080` or `http://localhost:8080`
3. You should see the medical chatbot interface
