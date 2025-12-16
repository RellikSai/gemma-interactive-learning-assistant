# Gemini PDF Reasoning Tool

This is a Streamlit app that:
- Reads PDFs
- Uses Gemini API to summarize and generate questions
- Generates content using custom AI personas

## How to Run

1. Install requirements
    : pip install -r requirements.txt

2. Create `.env` file
    : GEMINI_API_KEY=your_api_key_here

3. Run app
    : streamlit run app.py


## API Key Disclaimer

This project uses the Google Gemini API.
API keys are loaded using environment variables and are not stored in the repository.
Users must provide their own API key.
