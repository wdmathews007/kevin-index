import sys
from pypdf import PdfReader
import re

def test(text):
    return 1

kevin_index = [
    (test, 2.0)
]

def calc_kevin_index(text):
    index = 0
    stat_vals = []

    for stat in kevin_index:
        val = stat[0](text)
        stat_vals.append(val)

        index += val * stat[1]

    return index, stat_vals

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a pdf file path.")
        quit()

    pdf_path = sys.argv[1]
    reader = PdfReader(pdf_path)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    print(text)
    index, vals = calc_kevin_index(text)

    print(f"Kevin index of this text is {index}")
