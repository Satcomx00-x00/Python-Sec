import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup  # Import BeautifulSoup

# URL to retrieve the captcha image
captcha_url = 'http://31.220.95.27:9002/captcha.php'
# Get the captcha image from the server
response = requests.get(captcha_url)
# Open the image using PIL
image = Image.open(BytesIO(response.content))
# Use pytesseract to extract text from the image
captcha_text = pytesseract.image_to_string(image, config="-c tessedit_char_whitelist=0123456789 --psm 6")

# Clean up the extracted text (remove any unwanted characters)
captcha_text = captcha_text.strip()

# Prepare the data payload for the POST request
form_data = {
    'flag': '1585',  # This should be an integer between 1000 and 2000
    'captcha': captcha_text,
}

# URL to submit the form
submit_url = 'http://31.220.95.27:9002/captcha1/'
# Post the data to the server
response = requests.post(submit_url, data=form_data)

# Use BeautifulSoup to parse the HTML response
soup = BeautifulSoup(response.text, 'html.parser')

# Print the parsed HTML to see if the form was submitted successfully
print(soup.prettify())
print("Captcha Solved as:", captcha_text)
