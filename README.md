# Instalily GTM Engineer Case Study

This project is a lead generation prototype built for DuPont Tedlar's Graphics & Signage team. It employs AI-powered data enrichment and personalized outreach to help surface, engage, and track key prospects.

## Features

- Finds relevant industry events and associated companies  
- Identifies key decision makers at each company  
- Infers company email formats or defaults to LinkedIn messaging  
- Generates custom outreach messages using OpenAI  
- Displays and tracks everything in an interactive dashboard  
- Automates follow-ups, reminders, and activity logging  

## To Run

1. Install dependencies:

   pip install -r requirements.txt

2. Add your OpenAI API key to a `.env` file in the root folder:

   OPENAI_API_KEY=your-api-key-here

   You can get a key from https://platform.openai.com/api-keys

3. Test your OpenAI connection:

   python src/test_openai.py

4. Run the data processing pipeline:

   python main.py

5. Launch the dashboard:

   streamlit run src/dashboard.py

## Outreach Modes

The system supports two methods of outreach:
- Email: Automatically inferred if a common company format is detected or configured  
- LinkedIn: Default method if no valid email format is available or LinkedIn is preferred  

## Project Structure

.
├── data/                # Input and output CSVs  
├── src/                 # Source code  
│   ├── dashboard.py     # Main Streamlit dashboard  
│   ├── generate_outreach.py  
│   ├── infer_email.py  
│   └── ...  
├── requirements.txt  
├── README.md  
└── .env                 # Your OpenAI key goes here

## AI Workflow

This app uses the OpenAI API (GPT-4) to:
- Generate tailored outreach messages for each contact  
- Draft follow-up messages based on timing  
- Personalize communication based on name, title, company, and industry  

