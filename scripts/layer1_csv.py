import csv
import json


def to_csv():
    fields = ["id", "title", "partition", "url", "instructions", "ingredients"]

    with open("../dataset/layer1.json", "r") as json_file:
        with open("../dataset/layer1.csv", "w") as csv_file:

            writer = csv.DictWriter(
                    csv_file,
                    delimiter=',',
                    fieldnames=fields,
                    quoting=csv.QUOTE_ALL
                    )

            writer.writeheader()

            for line in json_file:
                try:
                    line = line[:-2]
                    d = json.loads(line)

                    ingr = ";".join([x["text"] for x in d["ingredients"]])
                    inst = ";".join([x["text"] for x in d["instructions"]])

                    writer.writerow({
                        "partition": d["partition"],
                        "url": d["url"],
                        "id": d["id"],
                        "title": d["title"],
                        "instructions": inst,
                        "ingredients": ingr
                    })

                except Exception as exc:
                    print(exc)

if __name__ == "__main__":
    to_csv()
