import csv
import hunterio_api
from urllib.parse import urlparse
import os
from api_keys import API_KEYS
from settings import LIMIT

cb_path = "companies-6-13-2018.csv"
out_path = "emails_searched_by_domain.csv"


def inject_contacts(companies, api_key):

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

            emails = hunterio_api.search_domain(item["domain"], api_key, limit=LIMIT)

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


def get_account_info():
    with open('api_key.txt', 'r') as f_txt:
        with open('api_keys.py', 'w') as f_py:
            f_py.write("API_KEYS = [\n")

            results = []
            for api_key in f_txt.readlines():
                api_key = api_key.rstrip()
                result = hunterio_api.fetch_account_info(api_key)
                if not len(result):
                    print("Fake api_key: " + api_key)
                    f_py.write("]")
                    return False

                results.append({'api_key': api_key, 'available': str(result[0]), 'reset_date': result[1]})

            results = sorted(results, key=lambda x:x['available'], reverse=True)
            for r in results:
                f_py.write("\t\t\t{'api_key':'" + r['api_key'] + "', 'available':'" + r['available'] + "', 'reset_date':'" + r['reset_date'] + "'},\n")
            f_py.write("]")

    print("Account information up-to-date!")
    return True

if __name__ == "__main__":
    if not get_account_info():
        exit(1)

    # cb_path = input("Crunchbase file path: ")
    companies = read_companies_csv(cb_path, out_path)
    # num = len(companies)
    num = 10
    count = 0
    key_idx = 0
    while count < num:
        available = int(API_KEYS[key_idx]["available"])

        if available == 0:
            print("Out of available api_keys! Please add more api_keys OR wait until the reset date!")
            break

        api_key = API_KEYS[key_idx]["api_key"]
        inject_contacts(companies[count:available-1 if available < num else num-1], api_key)
        count += available
        key_idx += 1

    get_account_info()
    print("Woohoo! Mission complete!")