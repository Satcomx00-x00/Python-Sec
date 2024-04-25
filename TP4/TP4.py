from pwn import remote
import base64, re


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
    if encoding == "base64":
        return base64.b64decode(data).decode()
    elif encoding == "morse":
        return Morse().decode(data)
    elif encoding == "hexadecimal":
        return bytes.fromhex(data).decode()


def encoding_detector(data):
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
    conn = remote("31.220.95.27", 13337)
    try:
        while True:
            server_message = conn.recv().decode().strip()
            print("Received:", server_message)

            if "A décoder:" in server_message:
                server_message = server_message.replace("A décoder: ", "")
                encoding_type, data = encoding_detector(server_message)
                if encoding_type:
                    print("Encoding type:", encoding_type)
                    decoded_message = decode_data(encoding_type, data)
                    print("Decoded:", decoded_message)
                    conn.sendline(decoded_message.encode())
                else:
                    print("Unknown encoding or data format")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
