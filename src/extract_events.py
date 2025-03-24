import csv
import os

def get_event_data():
    return [
        {
            "event": "FESPA",
            "company": "3M",
            "industry": "Commercial Graphics & Films",
            "website": "https://www.3m.com",
            "rationale": "Global leader in advanced vinyls and protective films with alignment to Tedlar signage use cases."
        },
        {
            "event": "ISASign Expo",
            "company": "Avery Dennison",
            "industry": "Graphics & Signage",
            "website": "https://graphics.averydennison.com",
            "rationale": "Dominant player in pressure-sensitive materials and architectural signage, with direct Tedlar overlap."
        },
        {
            "event": "Tape Week",
            "company": "Flexcon",
            "industry": "Adhesive Films & Industrial Graphics",
            "website": "https://www.flexcon.com",
            "rationale": "Specializes in durable, printable films with clear synergy to protective signage applications."
        },
        {
            "event": "FESPA",
            "company": "Arlon Graphics",
            "industry": "Vehicle Wraps & Signage",
            "website": "https://www.arlon.com",
            "rationale": "Focus on high-end performance wraps and flexible signage products overlaps with Tedlar value props."
        },
        {
            "event": "ISASign Expo",
            "company": "Orafol",
            "industry": "Adhesive Vinyls & Signage",
            "website": "https://www.orafol.com",
            "rationale": "Known for weather-resistant graphic solutions across automotive and architectural signage."
        },
        {
            "event": "Printing United",
            "company": "Nekoosa",
            "industry": "Print Media & Sign Materials",
            "website": "https://www.nekoosa.com",
            "rationale": "Offers specialty print substrates and signage products with shared use cases as Tedlar."
        },
        {
            "event": "Craig-Hallum Alpha Select Conference",
            "company": "LSI Industries",
            "industry": "Lighting & Signage Solutions",
            "website": "https://www.lsicorp.com",
            "rationale": "Manufacturer of illuminated signage systems in commercial, retail and petroleum markets."
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
    print(f"Saved {len(data)} entries to data/events_companies.csv")

