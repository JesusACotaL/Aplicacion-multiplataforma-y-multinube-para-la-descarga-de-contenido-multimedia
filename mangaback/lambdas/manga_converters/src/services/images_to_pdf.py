import os
import re
from fpdf import FPDF


def human_sort(l: list)-> list:
    """
    Sort list humanly

    Args:
        l (List): list to sort

    """
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key)]
    l.sort(key=alphanum)
    return l

def convert_images_to_pdf(input_folder: str, output_folder: str, book_name: str) -> None:
    """"""
    pdf = FPDF("P", "mm", "letter")
    images_list = os.listdir(input_folder)
    images_list = human_sort(images_list)

    pdf.set_x(60)
    for image in images_list:
        pdf.add_page()
        pdf.image(f"{input_folder}/{image}", 0, 0, 216, 279)
    pdf.output(f"{output_folder}/{book_name}.pdf", "F")