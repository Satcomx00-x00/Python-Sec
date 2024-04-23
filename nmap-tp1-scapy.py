#! /usr/bin/env python3

from scapy.all import *


def create_packet(target_ntwk):
    """
    Créez un paquet ARP avec l'adresse IP cible donnée.
    Args:
        target_ntwk (str): L'adresse IP de la cible.
    Returns:
        scapy.packet.Packet: Le paquet ARP.
    """
    arp = ARP(pdst=target_ntwk)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    return packet


def get_network_clients(packet):
    """
    Récupère la liste des clients du réseau en envoyant un paquet et en capturant les réponses.
    Args:
        packet: Le paquet à envoyer pour le balayage du réseau.
    Returns:
        Une liste de dictionnaires, où chaque dictionnaire représente un client du réseau.
        Chaque dictionnaire contient les adresses 'ip' et 'mac' du client.
    """
    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []
    for sent, received in result:
        clients.append({"ip": received.psrc, "mac": received.hwsrc})
    return clients


def scan_ports(ip):
    """
    Balaye les ports spécifiés pour l'adresse IP donnée.
    Args:
        ip (str): L'adresse IP à balayer.
    Returns:
        None
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
    Prints the available devices in the network along with their IP and MAC addresses.
    Args:
        clients (list): A list of dictionaries containing information about the clients.
            Each dictionary should have 'ip' and 'mac' keys representing the IP and MAC addresses respectively.
    Returns:
        None
    """
    print(f"Available devices in the network:")
    print(f"{'IP':16}    MAC")
    for client in clients:
        print("{:16}    {}".format(client["ip"], client["mac"]))


def main():
    ports = []
    target_ntwk = "10.33.0.0/24"
    print(f"Scanning network clients on network ==>> {target_ntwk}")
    packet = create_packet(target_ntwk)
    clients = get_network_clients(packet)
    for client in clients:
        print(f"Scanning ports for {client['ip']}")
        ports = scan_ports(client["ip"])
    print_clients(clients)
    print(f"Opened ports: {ports}")


if __name__ == "__main__":
    main()
