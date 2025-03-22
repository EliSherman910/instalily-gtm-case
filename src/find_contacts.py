import csv
import os

company_contacts = {
    "Avery Dennison": [
        {
            "name": "Tina Morales",
            "title": "Head of Product Development",
            "linkedin_url": "https://www.linkedin.com/in/tina-morales-dev/"
        },
        {
            "name": "Sean McCarthy",
            "title": "Director of Innovation",
            "linkedin_url": "https://www.linkedin.com/in/sean-mccarthy-innovate/"
        }
    ],
    "3M Commercial Graphics": [
        {
            "name": "Priya Desai",
            "title": "VP of Product Strategy",
            "linkedin_url": "https://www.linkedin.com/in/priya-desai-3m/"
        },
        {
            "name": "Lucas Chen",
            "title": "Lead R&D Engineer",
            "linkedin_url": "https://www.linkedin.com/in/lucas-chen-rnd/"
        }
    ],
    "Orafol": [
        {
            "name": "Megan Blake",
            "title": "Commercialization Manager",
            "linkedin_url": "https://www.linkedin.com/in/megan-blake-orafol/"
        },
        {
            "name": "Andre Silva",
            "title": "Senior Materials Scientist",
            "linkedin_url": "https://www.linkedin.com/in/andre-silva-materials/"
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

