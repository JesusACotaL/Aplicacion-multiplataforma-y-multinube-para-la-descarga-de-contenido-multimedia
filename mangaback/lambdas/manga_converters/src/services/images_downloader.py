from email.mime import base
from typing import List
from os.path import basename
from urllib import response
import requests

class ImagesDownloaderException(Exception):
    pass


class ImagesDownloader():
    def __init__(self, request_headers: dict= None) -> None:
        self.request_headers = request_headers or {}
        

    def download_images(self, images_urls: List[str], output_path: str):
        for img_url in images_urls:
            try:
                image_response = requests.get(img_url, stream=True, headers=self.request_headers)
                image_response.raise_for_status()

            except requests.exceptions.HTTPError as error:
                print(f"Failed to download image from url {img_url}")
                raise ImagesDownloaderException(error) from error

            with open(f"{output_path}/{basename(img_url)}", "wb") as img_file:
                img_file.write(image_response.content)


            
            
        