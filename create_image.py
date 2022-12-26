import os
import json
import uuid
from pathlib import Path
from base64 import b64decode

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_DIR = Path.cwd() / "responses"
DATA_DIR.mkdir(exist_ok=True)

def get_image_description()-> str:
    description = input("Please describe the image you want and hit <enter>: ")

    return description

def generate_image(image_description: str, number_of_images: int=1, size_of_image: str ="256x256")-> str:
    try:
        response = openai.Image.create(
            prompt=image_description,
            n=number_of_images,
            size=size_of_image,
            response_format="b64_json"
        ) 

        return response


    except Exception as error:
        print(error)


def save_to_file(image_json:json)-> Path:
    file_name = DATA_DIR / f"{uuid.uuid4()}-{image_json['created']}.json"

    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(image_json, file)

    return file_name

def write_to_png(file_name: Path)-> None:
    JSON_FILE = DATA_DIR / file_name

    IMAGE_DIR = Path.cwd() / "images" / JSON_FILE.stem
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
       response = json.load(file)

    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
        with open(image_file, mode="wb") as png:
            png.write(image_data)


if __name__ == "__main__":
    image_description = get_image_description()

    image_json= generate_image(image_description)

    file_name = save_to_file(image_json)

    write_to_png(file_name)
