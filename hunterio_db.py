import csv
import hunterio_api
from urllib.parse import urlparse

filename = "companies-6-13-2018.csv"

def injest_contacts():
    companies = read_csv(filename)

    with open('emails_searched_by_domain.csv', 'w') as f:

        fieldnames = ['Organization Name', 'Generic Email', 'Position', 'Name', 'Email', 'Phone Number', 'LinkedIn', 'Twitter']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in companies:
            generic_emails = ""
            personal_emails = []

            emails = hunterio_api.search_domain(item["domain"], limit=100)
            for e in emails:
                print(e)
                if e["type"] == "generic":
                    generic_emails += e["value"] + " (confidence: )" + str(e["confidence"]) + "\n"
                else:

                    position = e["position"] if e["position"] is not None else ""
                    name = e["first_name"] + " " + e["last_name"] if e["first_name"] is not None else ""
                    email = e["value"]
                    confidence = e["confidence"]
                    phone_number = e["phone_number"] if e["phone_number"] is not None else ""
                    linkedin = e["linkedin"] if e["linkedin"] is not None else ""
                    twitter = e["twitter"] if e["twitter"] is not None else ""

                    D = {'Position': position,
                         'Name': name,
                         'Email': email,
                         'Confidence': confidence,
                         'Phone Number': phone_number,
                         'LinkedIn': linkedin,
                         'Twitter': twitter
                         }

                    personal_emails.append(D)
        if len(personal_emails):
            writer.writerow({'Organization Name': item["org_name"].encode('utf8'),
                 'Generic Emails': generic_emails
                 }.update({k:v.encode('utf8') for k,v in personal_emails[0].items()}))

        if len(personal_emails) > 1:
            writer.writerow({k: v.encode('utf8') for k, v in personal_emails[1:].items()})

def read_csv(filename):
    companies = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            org_name = row['Organization Name']
            domain = urlparse(row['Website']).netloc
            founders = [x.lstrip() for x in row['Founders'].split(',')]

            companies.append({'idx':idx, 'org_name': org_name, 'domain': domain, 'founders': founders})

    return companies



if __name__ == "__main__":
    # pass
    # read_csv("companies-6-13-2018.csv")
    injest_contacts()