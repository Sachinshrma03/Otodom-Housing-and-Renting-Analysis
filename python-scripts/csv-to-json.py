import json
import csv

csvfile = open(
    "otodom_data.csv",
    "r",
    encoding="utf-8",
)
jsonfile = open(
    "otodom_data.json", "w"
)
fieldnames = (
    "id",
    "title",
    "estate",
    "transaction",
    "city",
    "province",
    "locations",
    "isPrivateOwner",
    "agency",
    "totalPrice",
    "rentPrice",
    "areaInSquareMeters",
    "roomsNumber",
    "dateCreated",
    "description",
)

reader = csv.DictReader(csvfile, fieldnames)

for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write("\n")
jsonfile.close()

print("Conversion complete")
