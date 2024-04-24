from PIL import Image
import pytesseract, requests, random
from bs4 import BeautifulSoup

session = requests.session()

def captcha1(URL, minimum, maximum, level):
    resp = session.get(URL)

    soup = BeautifulSoup(resp.text, 'html.parser')

    images = soup.find('img')

    if images and 'src' in images.attrs:
        # Construire l'URL complète de l'image si nécessaire
        img_url = requests.compat.urljoin(URL, images['src'])
        
        # Faire une autre requête pour télécharger l'image
        img_response = session.get(img_url)
        img_response.raise_for_status()
        
        # Sauvegarder l'image dans un fichier local
        with open("captcha.png", 'wb') as file:
            file.write(img_response.content)

    captcha = pytesseract.image_to_string(Image.open('captcha.png'))
    print(captcha)

    number = random.randint(minimum, maximum)

    resp = session.post(URL, data={'captcha': captcha, 'number': number})
    if "Incorrect flag." in resp.text:
        print("Incorrect flag.")
    else:
        print(f"All done for level {level}.")


for x in range(6):
    minimum = x+1 * 1000
    maximum = minimum + 1000
    captcha1(f'http://31.220.95.27:9002/captcha{x+1}/', minimum, maximum, x+1)