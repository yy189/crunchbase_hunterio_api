import csv
import hunterio_api
from urllib.parse import urlparse
import os

cb_path = "companies-6-13-2018.csv"
out_path = "emails_searched_by_domain.csv"

def injest_contacts():
    companies = read_companies_csv(cb_path, out_path)

    exists = False
    if os.path.isfile(out_path):
        exists = True

    with open(out_path, 'a+') as f:

        fieldnames = ['Organization Name', 'Generic Emails', 'Position', 'Name', 'Email', 'Confidence', 'Phone Number', 'LinkedIn', 'Twitter']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if exists:
            os.system("echo '\n' >> " + out_path)
        else:
            writer.writeheader()

        for item in companies:
            print(item)

            generic_emails = ""
            personal_emails = []

            emails = hunterio_api.search_domain(item["domain"], limit=10)

            for e in emails:
                print(e)

                if e["type"] == "generic":
                    generic_emails += e["value"] + " (confidence:" + str(e["confidence"]) + ")\n"
                else:
                    position = e["position"] if e["position"] is not None else ""
                    name = e["first_name"] + " " + e["last_name"] if e["first_name"] is not None else ""
                    email = e["value"]
                    confidence = str(e["confidence"])
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

            temp = {'Organization Name': item["org_name"], 'Generic Emails': generic_emails[:-1]}
            if (len(personal_emails)):
                temp.update({k: v for k, v in personal_emails[0].items()})
            writer.writerow(temp)


            if len(personal_emails) > 1:
                for pe in personal_emails[1:]:
                    writer.writerow({k: v for k, v in pe.items()})

            print()


def read_companies_csv(cb_path, out_path):

    existing_companies = read_existing_companies(out_path)
    companies = []
    with open(cb_path, 'r') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            org_name = row['Organization Name']
            if org_name not in existing_companies:
                domain = urlparse(row['Website']).netloc
                founders = [x.lstrip() for x in row['Founders'].split(',')]

                companies.append({'org_name': org_name, 'domain': domain, 'founders': founders})

    return companies

def read_existing_companies(filename):
    existing_companies = set('')

    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_companies.add(row['Organization Name'])

    return existing_companies

if __name__ == "__main__":
    # pass
    # read_csv("companies-6-13-2018.csv")
    injest_contacts()