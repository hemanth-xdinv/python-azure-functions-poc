import logging
import json, os, csv, pymongo, urllib
from pymongo import MongoClient
import azure.functions as func

def convert_data_to_csv():

    username = urllib.parse.quote_plus(os.environ.get("MONGO_USERNAME"))
    password = urllib.parse.quote_plus(os.environ.get("MONGO_PASSWORD"))

    print(username, password)
    url = f'mongodb+srv://{username}:{password}@cluster0-practice.tmxrp.azure.mongodb.net/practice-database?retryWrites=true&w=majority'

    cluster = MongoClient(url)

    db = cluster["practice-database"]
    student = db["student"]

    data = list(student.find({})) # Wrapping the cursor object(possibly a generator) to a list.

    with open("data.csv", "w") as new_csv_file:
        csv_writer = csv.writer(new_csv_file)
        csv_writer.writerow(data[0].keys()) # Writing the first row to be the fields.
        for data_point in data:
            print(data_point)
            csv_writer.writerow(data_point.values())


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    convert = req.params.get('convert')
    if not convert:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            convert = req_body.get('convert')

    if convert:
        convert_data_to_csv()
        return func.HttpResponse(f"The student data from the database has been convered to csv succesfully!")
    else:
        return func.HttpResponse(
             "The function triggered successfully. Pass a convert=true value in the query string or in the request body for converting the data in database to csv.",
             status_code=200
        )
