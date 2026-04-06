import socket
import time

TARGET_IP = "192.168.0.19"
PORT = 1999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

# Ping mit ID 00 00
packet = bytes([0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

print("Versuche Login nach Neustart...")
try:
    sock.sendto(packet, (TARGET_IP, PORT))
    data, addr = sock.recvfrom(1024)
    print(f"Antwort: {data.hex()}")
    
    if len(data) >= 4 and data[5] == 0: # Byte 5 ist Status (00 = OK)
        print(f"✅ ERFOLG! Neue Session ID: {hex(data[2])} {hex(data[3])}")
    elif len(data) >= 6 and data[5] == 4:
        print("❌ Immer noch Fehler 04: Der Master ist noch blockiert.")
except Exception as e:
    print(f"Fehler: {e}")