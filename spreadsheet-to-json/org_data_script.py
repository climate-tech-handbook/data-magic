import csv, json, os


def parse_csv_into_json(input_file, output_file):
    with open(input_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        data = []
        for row in reader:
            if row["UID"].strip():
                has_data = False
                new_row = {}
                for key, val in row.items():
                    if not key.strip():
                        continue  # Skip the empty key
                    if not val.strip():
                        new_row[key] = "N/A"
                    else:
                        new_row[key] = val
                        has_data = True
                if has_data:
                    data.append(new_row)

    with open(output_file, "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
        return data


json_org_data = parse_csv_into_json("org_data.csv", "org_data.json")
print(json_org_data)
