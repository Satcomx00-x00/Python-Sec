# TP4
from pwn import remote
import base64, re


# La classe « Morse » en Python fournit des fonctionnalités permettant de décoder le code Morse en
# texte brut.
class Morse:
    def __init__(self):
        self.MORSE_CODE_DICT = {
            "a": ".-",
            "b": "-...",
            "c": "-.-.",
            "d": "-..",
            "e": ".",
            "f": "..-.",
            "g": "--.",
            "h": "....",
            "i": "..",
            "j": ".---",
            "k": "-.-",
            "l": ".-..",
            "m": "--",
            "n": "-.",
            "o": "---",
            "p": ".--.",
            "q": "--.-",
            "r": ".-.",
            "s": "...",
            "t": "-",
            "u": "..-",
            "v": "...-",
            "w": ".--",
            "x": "-..-",
            "y": "-.--",
            "z": "--..",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
            ", ": "--..--",
            ".": ".-.-.-",
            "?": "..--..",
            "/": "-..-.",
            "-": "-....-",
            "(": "-.--.",
            ")": "-.--.-",
        }

        self.MORSE_CODE_DICT_REVERSED = {
            value: key for key, value in self.MORSE_CODE_DICT.items()
        }

    def decode(self, data):
        return "".join([self.MORSE_CODE_DICT_REVERSED.get(i) for i in data.split()])


def decode_data(encoding, data):
    """
    La fonction `decode_data` décode les données en fonction de la méthode de codage spécifiée (base64, morse ou hexadécimal).

    :param encoding: Le paramètre `encoding` spécifie le type de codage utilisé pour les données.
    :param data: Les données à décoder.
    :return: Les données décodées en fonction de l'encodage spécifié.
    """
    if encoding == "base64":
        return base64.b64decode(data).decode()
    elif encoding == "morse":
        return Morse().decode(data)
    elif encoding == "hexadecimal":
        return bytes.fromhex(data).decode()


def encoding_detector(data):
    """
    La fonction `encoding_detector` tente d'identifier le type de codage (hexadécimal, base64, morse) des données d'entrée.

    :param data: Fonction pour détecter le type de codage des données d'entrée.
    """
    if re.fullmatch(r"[0-9A-Fa-f]+", data) and not re.search(r"[G-Zg-z+/]", data):
        return "hexadecimal", data
    if re.fullmatch(
        r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$", data
    ):
        return "base64", data
    if re.fullmatch(r"[\.\- ]+", data):
        return "morse", data
    return None, data


def main():
    """
    La fonction principale établit une connexion à un serveur distant, reçoit des messages, décode les
    données codées et se termine lorsqu'un message d'indicateur est reçu.
    """
    # Invocation du socket pour se connecter au serveur distant
    conn = remote("31.220.95.27", 13337)
    try:
        while True:
            encoding_type = None
            # Réception des messages du serveur distant
            server_message = conn.recv().decode().strip()
            print("Received:", server_message)

            if "A décoder:" in server_message:
                server_message = server_message.replace("A décoder: ", "")
                # Détection du type de codage et décodage des données
                encoding_type, data = encoding_detector(server_message)

                if encoding_type:
                    print("Encoding type:", encoding_type)
                    # Décodage des données en fonction du type de codage détecté
                    decoded_message = decode_data(encoding_type, data)
                    print("Decoded:", decoded_message)
                    # Envoi du message décodé au serveur distant
                    conn.sendline(decoded_message.encode())
            elif "Flag" in server_message:
                exit()

    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Fermeture de la connexion
        conn.close()


if __name__ == "__main__":
    main()

# GG ! Flag : ESGI{G00d_Pr0gr4mmer}
