import os
from src.extract_events import save_to_csv, get_event_data
from src.find_contacts import load_companies, generate_contacts, save_contacts
from src.infer_email import process_contacts as process_emails
from src.generate_outreach import process_messages

def main():
    print("🔍 Extracting event/company data...")
    events = get_event_data()
    save_to_csv(events)

    print("👤 Generating contacts...")
    companies = load_companies()
    contacts = generate_contacts(companies)
    save_contacts(contacts)

    print("✉️ Inferring emails (or defaulting to LinkedIn)...")
    process_emails()

    print("💬 Generating outreach messages...")
    process_messages()

    print("\n✅ Pipeline complete. Final data saved to: data/contacts_with_messages.csv")

if __name__ == "__main__":
    main()

