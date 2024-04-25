#!/usr/bin/env python
# coding=utf-8

RED = "\033[31m"
RESET = "\033[0m"


def error():
    print(RED)
    print("[!] Input error.")
    exit(1)


def encode():
    """
    La fonction « encode » prend les entrées de l'utilisateur, les encode au format shellcode et imprime
    la sortie.
    """
    data = input("[<-] Input data to encode: ")
    print("[->] Output shellcode: ")
    shellcode = ""
    for char in data:
        shellcode += "\\x" + char.encode("hex")
    print(RED)
    print(shellcode)
    exit(0)


def decode():
    """
    La fonction `decode` prend les entrées de l'utilisateur, supprime les caractères "\x", décode les
    données au format hexadécimal et imprime le résultat décodé en rouge.
    """
    data = input("Input data to decode: ")
    if data.find("\\x") == -1:
        error()
    data = data.replace("\\x", "")
    try:
        plain = data.decode("hex")
    except TypeError as e:
        error()
    print(RED)
    print(plain)
    exit(0)


def main():
    """
    La fonction principale invite l'utilisateur à choisir entre l'encodage et le décodage du shellcode.
    """
    print("ShellCode encode decode")
    mode = input(
        "[<-] Input %s1[encode]%s or %s2[decode]%s:" % (RED, RESET, RED, RESET)
    )
    if mode == "1" or mode == "encode":
        encode()
    elif mode == "2" or mode == "decode":
        decode()
    else:
        error()


if __name__ == "__main__":
    main()
