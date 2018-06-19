import requests
import time
import urllib

base_url = "https://api.hunter.io/v2/"


def send_request(url, query_args, extractor):
    results = []

    try:
        response = requests.get(url, params=query_args)
        data = response.json()
        results.extend(extractor(data))
    except Exception as e:
        # import pdb;
        # pdb.set_trace()
        # time.sleep(10)
        print(e)
    return results



# search all the email addresses corresponding to one website
def search_domain(domain, api_key, limit=10):
    full_url = urllib.parse.urljoin(base_url, "domain-search")
    query_args = {"domain": domain, "limit": limit, "api_key": api_key}

    def contact_extractor(data):
        results = []
        for idx, email in enumerate(data["data"]["emails"]):
            results.append(email)
        return results

    results = send_request(full_url, query_args, contact_extractor)
    return results

def fetch_account_info(api_key):
    full_url = urllib.parse.urljoin(base_url, "account")
    query_args = {"api_key": api_key}

    def info_extractor(data):
        # returning [available, reset_date]
        return [data["data"]["calls"]["available"] - data["data"]["calls"]["used"], data["data"]["reset_date"]]

    results = send_request(full_url, query_args, info_extractor)
    return results



# generates or retrieves the most likely email address
# def find_email(domain, name, limit=10):
#     full_url = urllib.parse.urljoin(base_url, "email-finder")
#     fl = name.split()
#     first_name = fl[0]
#     last_name = fl[-1]
#     query_args = {"domain": domain, "first_name": first_name, "last_name": last_name, "api_key": api_key}
#
#     def email_extractor(data):
#         pass
#
#     results = send_request(full_url, query_args, email_extractor)
#     return results

# verify the deliverability of an email address
# def verify_email(email):
#     full_url = urllib.parse.urljoin(base_url, "email-verifier")
#     query_args = {"email": email, "api_key": api_key}
#
#     results = send_request(full_url, query_args)
#     return results