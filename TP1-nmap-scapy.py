#! /usr/bin/env python3

from scapy.all import ARP, Ether, srp, IP, TCP, sr1
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def create_packet(target_ntwk):
    """
    Crée un paquet ARP avec l'adresse IP cible donnée.
    :param target_ntwk: L'adresse IP de la cible.
    :return: Le paquet ARP.
    """
    arp = ARP(pdst=target_ntwk)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    return packet

def get_network_clients(packet):
    """
    Récupère la liste des clients du réseau en envoyant un paquet et en capturant les réponses.
    :param packet: Le paquet à envoyer pour le balayage du réseau.
    :return: Une liste de dictionnaires, chaque dictionnaire représente un client du réseau.
    """
    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in result:
        clients.append({"ip": received.psrc, "mac": received.hwsrc})
    return clients

def scan_ports(ip):
    """
    Balaye les ports spécifiés pour l'adresse IP donnée.
    :param ip: L'adresse IP à balayer.
    :return: Une liste des ports ouverts sur l'adresse IP spécifiée.
    """
    opened_ports = []
    print(f"Scanning ports for {ip}")
    for port in range(1, 1025):
        packet = IP(dst=ip) / TCP(dport=port, flags="S")
        response = sr1(packet, timeout=1, verbose=0)
        if response:
            opened_ports.append(port)
    return opened_ports

def print_clients(clients):
    """
    Imprime les adresses IP et MAC des clients dans le réseau.
    :param clients: Une liste de dictionnaires contenant les informations des clients.
    """
    print(f"Devices in the network:")
    print(f"{'IP':16}    MAC")
    for client in clients:
        print("{:16}    {}".format(client["ip"], client["mac"]))

def main():
    """
    Analyse les clients réseau sur un réseau spécifié, analyse les ports de chaque client et imprime les résultats.
    """
    ports = []
    target_ntwk = "10.33.0.0/24"
    network = ipaddress.ip_network(target_ntwk, strict=False)
    print(f"Scanning network clients on network ==>> {target_ntwk}")
    packet = create_packet(target_ntwk)
    clients = get_network_clients(packet)
    for client in clients:
        print(f"Scanning ports for {client['ip']}")
        ports.extend(scan_ports(client["ip"]))
    print_clients(clients)
    print(f"Opened ports: {ports}")

if __name__ == "__main__":
    main()
