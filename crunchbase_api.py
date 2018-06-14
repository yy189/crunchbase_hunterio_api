import requests
import time
import urllib

api_key = ""
base_url = "https://api.crunchbase.com/v3.1/"
path_prefix = "https://www.crunchbase.com/organization"

def request_all_pages(url, query_args, extractor, max_pages=None):
    results = []
    page_size = None
    while True:
        # Make request and add response to result set
        try:
            response = requests.get(url, params=query_args)
            data = response.json()
            results.extend(extractor(data))
        except Exception as e:
            import pdb;
            pdb.set_trace()
            time.sleep(10)

        # If we have paged through all the results, exit
        current = int(data["data"]["paging"]["current_page"])

        this_page_size = len(data["data"]["items"])
        if page_size is None and this_page_size == 0:
            print("No results on first page of request for url: %s" % url)
            raise Exception()

        page_size = page_size if page_size is not None else this_page_size
        total_items = int(data["data"]["paging"]["total_items"])
        if current * page_size >= total_items:
            break

        if max_pages is not None and current >= max_pages:
            break

        query_args["page"] = str(current + 1)

    return results

def fetch_companies(start_page=1, max_pages=None, filters={}):
    if not len(filters):
        filter = {"locations": "United States"}

    full_url = urllib.parse.urljoin(base_url, "odm-organizations")
    query_args = {"user_key": api_key, "page": str(start_page)}

    def company_extractor(data):
        results = []
        for idx, item in enumerate(data["data"]["items"]):
            if item["properties"]["primary_role"] != "company":
                print("Not a company: %s" % item["properties"]["name"])
                continue
            results.append(item)
        # print("\n".join(item["properties"]["name"] for item in results))
        return results

    results = request_all_pages(full_url, query_args, company_extractor, max_pages)
    return results