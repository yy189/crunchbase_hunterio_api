import crunchbase_api
import os


from pymongo import MongoClient
mongo_url = 'mongodb://localhost:27017/'
DATABASE = 'python-db'
TABLE = 'python-collection'

client = MongoClient(mongo_url)
db = client[DATABASE]
db.drop_collection(TABLE)
collection = db[TABLE]

def restart_mongodb_service():
    os.system(
        'brew services restart mongodb')

def stop_mongodb_service():
    os.system(
        "mongo --eval \"db.getSiblingDB('admin').shutdownServer()\"")

def save_db():
    fields = 'name,organization_name_url,company_linkedin,company_website,headquarter_location,description'

    # delete existing csv
    os.system(
        'rm test.csv'
    )

    # mongodb to csv
    os.system(
        'mongoexport --host localhost --db ' + DATABASE + ' --collection ' + TABLE + ' -f ' + fields + ' --type=csv -o test.csv')

    # change encoding to export accented words correctly
    os.system(
        'iconv -c -f utf-8 -t iso-8859-1 test.csv > output.csv')



def insert_company(company_uuid, company):
    keys = (["company_uuid", "name", "organization_name_url", "company_linkedin", "company_website",
             "headquarter_location", "description"
             ])

    headquarter_location = ""
    if company["city_name"] is not None:
        headquarter_location += company["city_name"]
    if company["region_name"] is not None:
        headquarter_location += ", " + company["region_name"]
    if company["country_code"] is not None:
        headquarter_location += ", " + company["country_code"]

    # url = company["homepage_url"]
    # if url is not None and url != "":
    #     parsed_url = parse.urlparse(url)
    #     url = parsed_url.scheme + "://" + parsed_url.netloc

    post = {
        "company_uuid": company_uuid,
        "name": company["name"],
        "organization_name_url": crunchbase_api.path_prefix + company["web_path"],
        "company_linkedin": company["linkedin_url"],
        "company_website": company["homepage_url"],
        "headquarter_location": headquarter_location,
        "description": company["short_description"]
    }

    post_id = collection.insert_one(post).inserted_id
    print("post id is ", post_id)


def inject_companies():
    current = 1
    batch_size = 10
    max_batches = 100
    while current * batch_size <= max_batches:
        companies = crunchbase_api.fetch_companies(start_page=current * batch_size, max_pages=(current + 1) * batch_size - 1, filters={"locations": "United States"})
        for c in companies:
            company_uuid = c["uuid"]
            company = c["properties"]
            insert_company(company_uuid, company)
        if not len(companies):
            break
        current += 1

