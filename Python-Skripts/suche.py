import socket
import time

# ------------------------------------------------------------------
# KONFIGURATION
# ------------------------------------------------------------------
TARGET_IP   = "192.168.0.19"
TARGET_PORT = 1999

# ID anpassen (falls Tool neu verbunden wurde)
ID_BYTE_1 = 0x02 
ID_BYTE_2 = 0x0b 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_single_byte_green(index):
    # Header: Länge 0x0F (wir machen das Paket extra lang: 15 Bytes)
    # Damit erreichen wir auch Bytes, die weit hinten liegen
    header = bytes([0x0F, 0x00, ID_BYTE_1, ID_BYTE_2, 0x00])
    
    # 10 Bytes Daten mit Nullen füllen
    data = bytearray([0x00] * 10)
    
    # Das Ziel-Byte auf Grün (01) setzen
    if index < 10:
        data[index] = 0x01
        
    packet = header + data
    sock.sendto(packet, (TARGET_IP, TARGET_PORT))

print(f"Starte erweiterten Such-Scan an {TARGET_IP}...")
print("Wann leuchtet die MITTE? (Bitte Nummer merken)")
print("-" * 40)

try:
    while True:
        # Wir scannen jetzt von 0 bis 8 durch
        for i in range(9):
            print(f"-> Byte {i} wird aktiviert...")
            send_single_byte_green(i)
            
            # 2 Sekunden Zeit zum Schauen
            time.sleep(2.0)
        
        print("-" * 40)
        print("Pause (Alles Aus)...")
        send_single_byte_green(99) # 99 = Aus
        time.sleep(1.0)

except KeyboardInterrupt:
    print("Ende.")
    send_single_byte_green(99)