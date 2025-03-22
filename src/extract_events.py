import csv
import os

def get_event_data():
    return [
        {
            "event": "ISASign Expo",
            "company": "Avery Dennison",
            "industry": "Graphics & Signage",
            "website": "https://graphics.averydennison.com",
            "rationale": "Major player in large format signage with overlap into Tedlar applications"
        },
        {
            "event": "FESPA Global Print Expo",
            "company": "3M Commercial Graphics",
            "industry": "Commercial Printing",
            "website": "https://www.3m.com",
            "rationale": "Produces durable vinyls and films aligned with Tedlar's protective applications"
        },
        {
            "event": "PRINTING United Expo",
            "company": "Orafol",
            "industry": "Adhesive Films & Signage",
            "website": "https://www.orafol.com",
            "rationale": "Active in vehicle wraps and weather resistant signage"
        }
    ]

def save_to_csv(data, filename="data/events_companies.csv"):
    os.makedirs("data", exist_ok=True)
    with open(filename, mode="w", newline="") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    data = get_event_data()
    save_to_csv(data)
    print(f"Saved {len(data)} entires to data/events_companies.csv")
