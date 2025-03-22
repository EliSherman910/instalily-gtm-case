import csv
import os

#We can set this to True later when we are ready to search google for the email formats
ENABLE_GOOGLE_EMAIL_FORMAT_LOOKUP = False

def get_domain_from_url(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        return domain.replace("www.", "")
    except:
        return None

#Placeholder for future email lookup
def lookup_email_format_online(company_name, domain):
    """
    Future implementation:
    If ENABLE_GOOGLE_EMAIL_FORMAT_LOOKUP is True:
    - Will search google with 
        "[{company name}] email format, site: rocketreach.com or hunter.io or signalhire.com or leadiq.com (which is my favorite because is free!)
    - Use tools like SerpAPI, BeautifulSoup, or scraping
    - Extract example email format that are most common (i.e. john.doe@company.com)
    - Use tools to identify common formats and return the format string (i.e. 'first.last')

    As of now will return nothing, but is a great opportunity for future enhancement!
    """
    return None

#Will include some foundation for when we add the google email lookup
def process_contacts(input_file="data/contacts.csv", output_file="data/contacts_with_emails.csv"):
    contacts = []

    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            website = row["company_website"]
            company = row["company"]
            domain = get_domain_from_url(website)

            #default to LinkedIn for now
            row["email"] = ""
            row["email_format"] = ""
            row["outreach_method"] = "linkedin"

            #for the future when we try finding the real email format via google search
            if ENABLE_GOOGLE_EMAIL_FORMAT_LOOKUP:
                format_found = lookup_email_format_online(company, domain)
                if format_found:
                    #would be something like this:
                    #row["email"] = infer_email(name, domain, format_found)
                    #row["email_format"] = format_found
                    #row["outreach_method"] = "email"
                    pass

            contacts.append(row)

    os.makedirs("data", exist_ok=True)
    with open(output_file, mode="w", newline="") as csvfile:
        fieldnames = contacts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(contacts)
    print(f"Processed {len(contacts)} contacts -> {output_file} (LinkedIn outreach only)")

if __name__ == "__main__":
    process_contacts()
