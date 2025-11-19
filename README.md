# GPT-5.1 Chatbot

A simple Streamlit chatbot application powered by OpenAI's GPT-5.1 model with full conversation memory.

## Features

- Real-time chat interface with GPT-5.1
- Full conversation history maintained throughout the session
- Fast response mode (reasoning: none)
- Clear conversation button to start fresh
- Clean and intuitive UI

## Project Structure

```
pathway-missionary-roleplay/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── venv/                     # Virtual environment (created during setup)
├── .env                      # API key (create from .env.example)
├── .env.example             # Template for API key setup
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

You can get your API key from: https://platform.openai.com/api-keys

### 5. Run the Application

```bash
python3 -m streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Subsequent Runs

After the initial setup, you only need to:

```bash
source venv/bin/activate
python3 -m streamlit run app.py
```

## Usage

1. Type your message in the chat input at the bottom
2. Press Enter to send your message
3. The chatbot will respond using GPT-5.1
4. All conversation history is maintained in the session
5. Use the "Clear Conversation" button in the sidebar to start a new conversation

## Technical Details

- **Model**: GPT-5.1
- **Reasoning Mode**: none (fast, low-latency responses)
- **Memory**: Session-based (resets on browser refresh)
- **API**: OpenAI Chat Completions API

## Notes

- The conversation history is stored in Streamlit's session state and will be lost when you refresh the browser
- Make sure your `.env` file is never committed to version control (already in `.gitignore`)
- Ensure you have sufficient OpenAI API credits for GPT-5.1 usage
- GPT-5.1 is OpenAI's newest flagship model with improved reasoning capabilities and faster response times
- The app uses `reasoning: { "type": "none" }` for low-latency, fast responses without extended reasoning
