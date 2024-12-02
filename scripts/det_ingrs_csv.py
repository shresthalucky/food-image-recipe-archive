import csv
import json
from itertools import compress

from tqdm import tqdm


def to_csv():
    
    det_ingrs = json.load(open("../dataset/det_ingrs.json", "r"));

    fields = ["id", "ingredients"]

    with open("../dataset/det_ingrs.csv", "w") as csv_file:

        writer = csv.DictWriter(
                csv_file,
                delimiter=',',
                fieldnames=fields,
                quoting=csv.QUOTE_ALL
                )

        writer.writeheader()

        for item in tqdm(det_ingrs):

            valid_ingrs = compress(item["ingredients"], item["valid"])
            
            writer.writerow({
                "id": item['id'],
                "ingredients": ";".join([ingredient["text"] for ingredient in valid_ingrs])
            })


if __name__ == "__main__":
    to_csv()
