import requests


def convert_docx_to_pdf(path_to_doc_file: str) -> bytes:
    url = 'http://localhost:3000/forms/libreoffice/convert'

    files = {'f': ('file.pdf', open(path_to_doc_file, 'rb'))}
    return requests.post(url, files=files).content
