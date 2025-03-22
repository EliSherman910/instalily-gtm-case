import csv
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_message(name, title, company, outreach_method, event=None, rationale=None):
    base_intro = f"{name} is the {title} at {company}."
    if event:
        base_intro += f" They are attending {event}."
    if rationale:
        base_intro += f" {company} was selected because \"{rationale}\"."    

    if outreach_method == "email":
        prompt = f"""
        Write a short but very personalized cold outreach email to {name}, the {title} at {company}.
        {base_intro}
        You are introduing a solution/product built on DuPont Tedlar, high durability protective films for signage, vehicle wraps and commercial graphics. 
        Make it relevant to their role and industry, and end with something encouraging them to connect such as "Would love to connect if this is relevant to your team." or something similar.
        """
    else:
        prompt = f"""
        Write a short, casual LinkedIn message to {name}, the {title} at {company}.
        {base_intro}
        Mention that you are reaching out about high performance protective films for signage, a commercial graphics, built with DuPont Tedlar. 
        Make the message conversational and light, like an actual direct message, with a low pressure encouragement to connect. 
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role":"user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating message for {name}: {e}")
        return ""

def process_messages(input_file="data/contacts_with_emails.csv", output_file="data/contacts_with_messages.csv"):
    contacts = []

    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["name"]
            title = row["title"]
            company = row["title"]
            outreach_method = row["outreach_method"]
            event = row.get("event", "")
            rationale = row.get("rationale", "")

            print(f"Generating message for {name} at {company} via {outreach_method}...")

            message = generate_message(name, title, company, outreach_method, event, rationale)
            row["outreach_message"] = message
            row["last_outreach_date"] = ""
            row["next_followup_date"] = ""
            row["followup_status"] = ""
            row["followup_message"] = ""

            contacts.append(row)

    os.makedirs("data", exist_ok=True)
    with open(output_file, mode="w", newline="") as csvfile:
        fieldnames = contacts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)

    print(f"Generated messages for {len(contacts)} contacts -> {output_file}")

if __name__ == "__main__":
    process_messages()
