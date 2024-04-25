from pwn import *



MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

# morse decoder
def morse_decoder(message):
    message += ' '
    decipher = ''
    citext = ''
    for letter in message:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''
    return decipher

# Establish a connection to the server
host = "31.220.95.27"
port = 13337
conn = remote(host, port)

try:
    # Receive data until "A décoder: " is found
    conn.recvuntil("A décoder: ")
    
    # Receive the actual data to decode, assuming it ends with a newline
    data_to_decode = conn.recvline().strip()  # Adjust `recv` method as needed
    
    # Decode the data as required
    # Example: If the data is base64 encoded, you would decode it like this:
    
    # Here you need to know the specific encoding or data type to properly decode it
    # For demonstration, I'm printing the received encoded data
    print("Data received to decode:", data_to_decode)
    
    # Process or decode the data here as necessary

finally:
    # Close the connection
    conn.close()
