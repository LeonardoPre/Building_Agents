import os
import random
import json

def load_dataset(path):
    """
    Load the dataset from the specified path.
    
    Args:
        path (str): The path to the dataset file.
        
    Returns:
        list: A list of dictionaries containing the dataset.
    """
    
    
    with open(path, 'r') as file:
        lines = file.readlines()
    
    return lines

def get_plants(path):
    """
    Get the list of plants from the dataset.
    
    Args:
        path (str): The path to the dataset file.
        
    Returns:
        list: A list of plant names.
    """
    
    filenames = os.listdir(path)
    plants = [os.path.splitext(line)[0] for line in filenames]
    return plants

def create_dataset(num_samples, filename="dataset.json"):
    """
    Create a dataset with a specified number of samples.
    
    Args:
        num_samples (int): The number of samples to create.
        
    Returns:
        list: A list of dictionaries containing the dataset.
    """
    
    plants = get_plants("beginn")
    print(plants)
    cities = load_dataset(os.path.join("dataset_creation", "cities.txt"))  
    dates = load_dataset(os.path.join("dataset_creation", "dates.txt"))
    sentences = load_dataset(os.path.join("dataset_creation", "sentences.txt"))
    additional_plants = ["Eichel", "Kastanie", "Linde", "Klatschmohn", "Raps"]

    plants.extend(additional_plants)
    plants_samples = [plant.title() for plant in plants for _ in range(50)]
    print(len(plants_samples))
    dataset = []
    for i, plant in enumerate(plants_samples):
        city = random.choice(cities).strip()
        date = random.choice(dates).strip()
        sentence = random.choice(sentences).strip()

        sentence= sentence.replace("<pflanze>", plant.title())
        sentence = sentence.replace("<berlin>", city)
        sentence = sentence.replace("<datum>", date)
        dataset.append({
            "plant": plant,
            "city": city,
            "date": date,
            "sentence": sentence,
            "id": i
        })

    
    with open (filename, "w", encoding="utf-8") as file:
        json.dump(dataset, file, indent=4)


if __name__ == "__main__":
    num_samples = 20
    filename = "datasets/dataset_850.json"
    create_dataset(num_samples, filename)



