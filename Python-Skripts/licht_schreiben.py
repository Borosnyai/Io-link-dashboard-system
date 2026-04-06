import socket
import time
import binascii

# ------------------------------------------------------------------
# KONFIGURATION
# ------------------------------------------------------------------
TARGET_IP   = "192.168.0.19"
TARGET_PORT = 1999
SPEED       = 0.2

# ------------------------------------------------------------------
# ID SETUP (Ihre letzte ID)
# ------------------------------------------------------------------
ID_BYTE_1 = 0x02 
ID_BYTE_2 = 0x0b 

# ------------------------------------------------------------------
# FARBEN (0=Aus, 1=Grün, 2=Rot)
# ------------------------------------------------------------------
VAL_OFF = 0
VAL_GRN = 1
VAL_RED = 2

# Animation: Oben -> Mitte -> Unten -> Mitte -> Oben
# Format: [Oben, Mitte, Unten]
frames = [
    [VAL_GRN, VAL_OFF, VAL_OFF], # Oben
    [VAL_OFF, VAL_GRN, VAL_OFF], # Mitte
    [VAL_OFF, VAL_OFF, VAL_GRN], # Unten
    [VAL_OFF, VAL_GRN, VAL_OFF], # Mitte (zurück)
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_packed(top, mid, bot):
    # BIT-MAGIE: Wir packen Oben und Mitte in Byte 0
    # Oben = Rechte 4 Bits
    # Mitte = Linke 4 Bits (deshalb mal 16 bzw. << 4)
    byte0_val = (mid << 4) | top
    
    # Unten kommt in Byte 1
    byte1_val = bot
    
    # Header: Länge 09, Zähler 00, ID, ID, 00
    header = bytes([0x09, 0x00, ID_BYTE_1, ID_BYTE_2, 0x00])
    
    # Payload: Byte0 (Oben+Mitte), Byte1 (Unten), Rest Nullen
    payload = bytes([byte0_val, byte1_val, 0x00, 0x00])
    
    sock.sendto(header + payload, (TARGET_IP, TARGET_PORT))

def send_off():
    # Alles aus -> 00 00
    send_packed(0, 0, 0)

# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
print(f"Starte Nibble-Lauflicht (Mitte repariert) an {TARGET_IP}...")
print("Jetzt sollte es flüssig laufen!")

try:
    while True:
        for frame in frames:
            # frame = [Oben, Mitte, Unten]
            send_packed(frame[0], frame[1], frame[2])
            time.sleep(SPEED)

except KeyboardInterrupt:
    print("\nStopp.")

finally:
    print("Licht aus.")
    for _ in range(5):
        send_off()
        time.sleep(0.05)
    sock.close()