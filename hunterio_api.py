import requests
import time
import urllib

base_url = "https://api.hunter.io/v2/"
api_key = ""


def send_request(url, query_args, extractor):
    results = []

    try:
        response = requests.get(url, params=query_args)
        data = response.json()
        results.extend(extractor(data))
    except Exception as e:
        import pdb;
        pdb.set_trace()
        time.sleep(10)

    return results



# search all the email addresses corresponding to one website
def search_domain(domain, limit=10):
    full_url = urllib.parse.urljoin(base_url, "domain-search")
    query_args = {"domain": domain, "limit": limit, "api_key": api_key}

    def contact_extracor(data):
        results = []
        for idx, email in enumerate(data["data"]["emails"]):
            results.append(email)
        return results

    results = send_request(full_url, query_args, contact_extracor)
    return results




# generates or retrieves the most likely email address
def find_email(domain, name, limit=10):
    full_url = urllib.parse.urljoin(base_url, "email-finder")
    fl = name.split()
    first_name = fl[0]
    last_name = fl[-1]
    query_args = {"domain": domain, "first_name": first_name, "last_name": last_name, "api_key": api_key}

    def email_extractor(data):
        results = []
        for idx, email in enumerate(data["data"]["emails"]):
            results.append(email)
        return results


    results = send_request(full_url, query_args, email_extractor)
    return results


# verify the deliverability of an email address
def verify_email(email):
    full_url = urllib.parse.urljoin(base_url, "email-verifier")
    query_args = {"email": email, "api_key": api_key}

    results = send_request(full_url, query_args)
    return results