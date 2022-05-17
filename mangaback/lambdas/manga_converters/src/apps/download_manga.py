from services.images_to_epub import EPubConverter
from services.images_downloader import ImagesDownloader
from utils.constants import IMAGES_REQUEST_HEADERS


def lambda_handler(event: dict, context: str):
    """
    lambda_handler for download_manga endpoint

    Args:
        event (dict): lambda event
        context (str): lambda context
    Returns:
        dict: Manga file response
    """
    print(event)
    print(context)

    request_body = event.get("body")

    temp_dir = "tmp"
    book_name = request_body.get('book_name')
    file_name = f"{request_body.get('book_name')}.epub"

    downloader = ImagesDownloader(request_headers=IMAGES_REQUEST_HEADERS)


    # downloader.download_images(request_body.get("images_urls"), temp_dir)
    converter = EPubConverter(master=None, input_dir="tmp", file=f"{temp_dir}/{file_name}", name=book_name, grayscale=False, max_width=None, max_height=None, wrap_pages=False)

    converter.run()

    return {"status": 200}



