mongoexport --host localhost --db python-db --collection python-collection -f name,organization_name_url,company_linkedin,company_website,headquarter_location,description --type=csv -o output.csv

iconv -c -f utf-8 -t iso-8859-1 output.csv > output.csv# crunchbase_hunterio_api
