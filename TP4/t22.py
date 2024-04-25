import morse_talk as morse  # You'll need to install this package for Morse code

encoded = "-... -. -.-- ...- -.-. ..... -.. -..- .. .- ...-- -. .---- ...- - -.- .--. -... -.... --.- -.. ...- -. .-. ---.. ----- .. .- .---- .---- ----. ...-"

def decode_data(encoding, data):
    if encoding == "morse":
        return morse.decode(data)
    else:
        return data
    
print(decode_data("morse", encoded))
