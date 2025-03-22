# Instalily GTM Engineer Case Study
This project is a lead generation prototype built for DuPont Tedlar's Graphics & Signage team that employs AI powered data enrichment and outreach.

##Features
- Finds relevant industry events and companies
- Finds key decision makers
- Determines email address format or prepares a LinkedIn outreach/direct message
- Generates personalized messages using OpenAI
- Displays results in an interactive dashboard

## To Run
1. Install dependancies

    ```bash
    pip install -r requirements.txt
    ```

2. Add your OpenAI API Key to a `.env` file in the root folder:

    ```env
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```

    > You can get your key from https://platform.openai.com/api-keys 

3. Test the OpenAI connection:
    ```bash
    python src/test_openai.py
    ```
4. Run the main script: 
    ```bash
    python main.py
    ```

5. Launch the dashboard
    ```bash
    streamlit run src/dashboard.py
    ```

##Outreach Modes
This system supports both email (if inferred from company format) or LinkedIn (if email is unavalibale or is preffered) 
