import os
import pandas
from functools import lru_cache
from enum import StrEnum
from typing import Annotated, Any
from langchain.tools import tool

class Bloom(StrEnum):
    """
    Enumeration for different bloom stages.
    """
    BEGINN = "beginn"
    ENDE = "ende"
    
    def __str__(self):
        return self.value


class Flower:
    """
    Represents a plant with its name and associated data.
    """

    def __init__(self, name: str):
        self.name = name

        with open(f"beginn/{name}.tsv", "r") as file:
            self.begin_data = pandas.read_csv(file, sep="\t", index_col=None)
            self.begin_data.columns = self.begin_data.columns.str.strip()
            self.begin_data.reset_index(drop=True, inplace=True)
        
        with open(f"beginn_info/{name}.txt", "r") as file:
            self.begin_info = file.read().strip()
        
        with open(f"ende/{name}.tsv", "r") as file:
            self.ende_data = pandas.read_csv(file, sep="\t", index_col=None)
            self.ende_data.columns = self.ende_data.columns.str.strip()
            self.ende_data.reset_index(drop=True, inplace=True)
        
        with open(f"ende_info/{name}.txt", "r") as file:
            self.ende_info = file.read().strip()
    
    def __repr__(self):
        return f"Flower(name={self.name})"
    
    def get_begin_dict(self) -> dict:
        """
        Convert the Flower instance to a dictionary representation for begin data.

        Returns:
            dict: A dictionary containing the name, data, and info of the plant.
        """
        return {
            "name": self.name,
            "data": self.begin_data,
            "info": self.begin_info
        }
    
    def get_ende_dict(self) -> dict:
        """
        Convert the Flower instance to a dictionary representation for end data.

        Returns:
            dict: A dictionary containing the name, data, and info of the plant.
        """
        return {
            "name": self.name,
            "data": self.ende_data,
            "info": self.ende_info
        }



def get_all_plants() -> list[str]:
    """
    Get all plant names from the 'beginn' directory.

    Returns:
        list[str]: A list of plant names without file extensions.
    """
    plants = [os.path.splitext(filename)[0] for filename in os.listdir('beginn') if filename.endswith('.tsv')]
    return " ".join(plants)

@lru_cache(maxsize=None)
def get_begin(plant: str) -> dict:
    """
    Get the Flower instance for a specific plant's begin data.

    Args:
        plant (str): The name of the plant.

    Returns:
        dict[str, any]: A dictionary containing the plant's name, flower data, and information.
    """
    plant = plant.lower()
    if plant not in get_all_plants():
        raise ValueError(f"Plant '{plant}' not found in 'beginn' directory.")
    return Flower(plant).get_begin_dict()


@lru_cache(maxsize=None)
def get_end(plant: str) -> dict:
    """
    Get the Flower instance for a specific plant's end data.

    Args:
        plant (str): The name of the plant.

    Returns:
        dict[str, any]: A dictionary containing the plant's name, flower data, and information.
    """
    if plant not in get_all_plants():
        raise ValueError(f"Plant '{plant}' not found in 'beginn' directory.")
    
    return Flower(plant).get_ende_dict()



def get_bloom_data(
    plant: str,
    year: int) -> dict:
    """
    Get bloom data for a specific plant for a given year. 
    The data gives the bloom start date for the specified year of a specific plant

    Args:
        plant (str): The name of the plant.
        year (int): The year for which to retrieve bloom data.

    Returns:
        dict: A dictionary containing bloom data and additional information.
    """
    
    df = get_begin(plant)["data"]
    info = get_begin(plant)["info"]
    
    bloom_data = df[df["Jahr"] == year]
    
    if not bloom_data.empty:
        return {"data": bloom_data.to_dict(), "info": info}
    else:
        return {"data": None, "info": "No data found for the given bloom number."}


# def get_bloom_data_whole(plant: Annotated[str, "The plant the current agent is responsible for"], year: int) -> dict:
#     """
#     Get bloom data for the Erle plant for a given year.

#     Args:
#         year (int): The year for which to retrieve bloom data.

#     Returns:
#         dict: A dictionary containing bloom data and additional information.
#     """
#     begin_data = get_bloom_data(plant.lower(), year, Bloom.BEGINN)
#     ende_data = get_bloom_data(plant.lower(), year, Bloom.ENDE)
#     #print(begin_data)
#     #print(ende_data["data"])
#     return {
#         "begin_data": begin_data["data"],
#         "ende_data": ende_data["data"],
#         "info_beginn": begin_data["info"],
#         "info_ende": ende_data["info"]
#     }