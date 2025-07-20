import json
import os
import pandas as pd
from datetime import datetime, timedelta
from answer import Answer

def load_dataset(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def load_bloom_data(file_path: str) -> pd.DataFrame:
    """
    Load bloom data from a TSV file into a pandas DataFrame.

    Args:
        file_path (str): Path to the TSV file.

    Returns:
        pd.DataFrame: DataFrame containing the bloom data.
    """
    # Load the TSV file
    bloom_data = pd.read_csv(file_path, sep="\t")
    # Strip column names to remove extra spaces
    bloom_data.columns = bloom_data.columns.str.strip()
    return bloom_data

def check_bloom(plant: str, date: str, id: int, deviation: int) -> dict:
    """
    Check if a plant is in bloom on a given date.

    Args:
        plant (str): Name of the plant.
        date (str): Date in the format "dd.mm.yyyy".

    Returns:
        dict: Information about the bloom status.
    """
    # Load the bloom data for the specified plant
    plant = plant.lower()
    tsv_name = f"beginn/{plant}.tsv"
    if not os.path.exists(tsv_name):
        return {
            "plant": plant,
            "date": date,
            "start_date": None,
            "id": id,
            "is_blooming": Answer.NO_ANSWER
        }

    bloom_start_data = load_bloom_data(tsv_name)

    #bloom_end_data = load_bloom_data(f"ende/{plant}.tsv")

    year = datetime.strptime(date, "%d.%m.%Y").year
    # Filter the data for the given year
    row_start = bloom_start_data[bloom_start_data["Jahr"] == year]
    #row_end = bloom_end_data[bloom_end_data["Jahr"] == year]

    start_date = row_start.iloc[:,1].values[0].strip() + f"{year}"
    #end_date = row_end.iloc[:,1].values[0].strip() + f"{year}"

    parsed_start_date = datetime.strptime(start_date, "%d.%m.%Y") - timedelta(days=deviation)
    #parsed_end_date = datetime.strptime(end_date, "%d.%m.%Y") + timedelta(days=deviation)

    parsed_date = datetime.strptime(date, "%d.%m.%Y")

    # Check if the parsed date is within the bloom period
    if parsed_start_date <= parsed_date:
        return {
            "plant": plant,
            "date": date,
            "start_date": start_date,
            "id": id,
            "is_blooming": Answer.YES
        }
    else:
        return {
            "plant": plant,
            "date": date,
            "start_date": start_date,
            "id": id,
            "is_blooming": Answer.NO
        }



if __name__ == "__main__":
    dataset = load_dataset("datasets/dataset_850.json")
    results = []
    for deviation in [0, 5, 10]:
        for entry in dataset:
            plant = entry["plant"]
            date = entry["date"]
            id = entry["id"]
            bloom_info = check_bloom(plant, date, id, deviation=deviation)
            results.append(bloom_info)
        # Save the results to a JSON file
        with open(f"ground_truth/ground_truth_850_dev_{deviation}.json", "w") as file:
            json.dump(results, file, indent=4)
    