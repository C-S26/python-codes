#show summary of packets using scapy
from scapy.all import sniff

def show(packet):
    #print(packet)
    print(packet.summary())

sniff(count=10, prn=show)
#python -m pip install scapy
