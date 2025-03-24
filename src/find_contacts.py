import csv
import os

company_contacts = {
    "Avery Dennison": [
        {
            "name": "Joshua Yelverton",
            "title": "Regional Manager at Avery Dennison Graphics Solutions",
            "linkedin_url": "https://www.linkedin.com/in/joshua-yelverton-48158b92/"
        },
        {
            "name": "Grant Bertoson",
            "title": "Regional Manager at Avery Dennison Graphics Solutions",
            "linkedin_url": "https://www.linkedin.com/in/grantbertoson/"
        }
    ],
    "3M Commercial Graphics": [
        {
            "name": "Christine Neutgens",
            "title": "Creative Lead - Graphics at 3M",
            "linkedin_url": "https://www.linkedin.com/in/christine-neutgens-3713198/"
        },
        {
            "name": "Eric Malmberg",
            "title": "Senior Account Executive Commercial Graphics",
            "linkedin_url": "https://www.linkedin.com/in/ericvmalmberg/"
        },
        {
            "name": "Jon Mansheim",
            "title": "3M Global Portfolio Director - Graphics",
            "linkedin_url": "https://www.linkedin.com/in/jon-mansheim-2017911/"
        }
    ],
    "Orafol": [
        {
            "name": "Tim Bennett",
            "title": "Managing Director - ORAFOL Canada Inc.",
            "linkedin_url": "https://www.linkedin.com/in/tim-bennett-59b54a17/"
        },
        {
            "name": "Dr. Sefan Pfirrmann",
            "title": "R&D Director Graphic Innovations bei ORAFOL Europe GmbH",
            "linkedin_url": "https://www.linkedin.com/in/dr-stefan-pfirrmann-ab875567/"
        },
        {
            "name": "Stephen Kampa",
            "title": "Executive Leadership | Business Development | Growing Sales in Asia",
            "linkedin_url": "https://www.linkedin.com/in/stephenkampa/"
        }
    ],
    "Arlon Graphics": [
        {
            "name": "Michelle Gunning",
            "title": "Vice President - EMEA and Global Growth",
            "linkedin_url": "https://www.linkedin.com/in/michellegunning/"
        },
        {
            "name": "Rebecca Chen",
            "title": "Global Product Management, Director",
            "linkedin_url": "https://www.linkedin.com/in/rebecca-chen-2b84a6126/"
        },
        {
            "name": "Jeff Goh",
            "title": "President Asia Pacific Arlon Graphics",
            "linkedin_url": "https://www.linkedin.com/in/jeffgohceo/"
        }
    ],
    "Flexcon": [
        {
            "name": "Michael Romanelli",
            "title": "Vice President, Innovation & Technology",
            "linkedin_url": "https://www.linkedin.com/in/mdromanelli/"
        },
        {
            "name": "Kevin Haughey",
            "title": "Sales Director, Central and West at Flexcon",
            "linkedin_url": "https://www.linkedin.com/in/kevin-haughey-1b972a6/"
        },
        {
            "name": "Jordan Smith",
            "title": "Growth Strategy, Sr. Manager",
            "linkedin_url": "https://www.linkedin.com/in/jordansmithflexcon/"
        }
    ],
    "Nekoosa": [
        {
            "name": "Scott Bell",
            "title": "Business Development Manager at Nekoosa",
            "linkedin_url": "https://www.linkedin.com/in/scott-bell-1334807/"
        },
        {
            "name": "Mike Bluell",
            "title": "Director Of Operations at Nekoosa",
            "linkedin_url": "https://www.linkedin.com/in/mike-bluell-70628517/"
        },
        {
            "name": "Bryan Baab",
            "title": "Product Development Manager - Wide Format Graphics at Nekoosa",
            "linkedin_url": "https://www.linkedin.com/in/bryan-baab-74487a10/"
        }
    ],
    "LSI Industries": [
        {
            "name": "Michael Prachar",
            "title": "Chief Marketing Officer",
            "linkedin_url": "https://www.linkedin.com/in/michaelapracharexecutive/"
        },
        {
            "name": "Nicole Stella",
            "title": "Vice President of Sales, National Accounts at LSI",
            "linkedin_url": "https://www.linkedin.com/in/nicole-stella-27a6656/"
        }
    ]
}

def load_companies(filename="data/events_companies.csv"):
    companies = []
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            companies.append(row)
    return companies

def generate_contacts(companies):
    contacts = []
    for company in companies:
        company_name = company["company"]
        website = company["website"]
        event = company.get("event", "")
        rationale = company.get("rationale", "")

        contact_list = company_contacts.get(company_name, [])

        for contact in contact_list:
            contacts.append({
                "name": contact["name"],
                "title": contact["title"],
                "linkedin_url": contact["linkedin_url"],
                "company": company_name,
                "company_website": website,
                "event": event,
                "rationale": rationale
            })
    return contacts

def save_contacts(contacts, filename="data/contacts.csv"):
    os.makedirs("data", exist_ok=True)
    with open(filename, mode="w", newline="") as csvfile:
        fieldnames = contacts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)

if __name__ == "__main__":
    companies = load_companies()
    contacts = generate_contacts(companies)
    save_contacts(contacts)
    print(f"Saved {len(contacts)} contacts to data/contacts.csv")

