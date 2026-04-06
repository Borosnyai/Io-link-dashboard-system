import socket
import struct
import time

TARGET_IP   = "192.168.0.19"
TARGET_PORT = 1999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

def get_session_id():
    print("Versuche, eine Session ID anzufordern...")
    
    # TRICK: Wir senden einen harmlosen Lese-Befehl (Vendor Name lesen)
    # mit einer "leeren" ID (00 00).
    # Header: Länge 0A, Zähler 00, ID 00 00, Rsv 00
    # ISDU Read: Index 10 (Vendor Name), Sub 0
    
    #               Len   Cnt   ID1   ID2   Rsv   IdxH  IdxL  Sub   Op    Len   Data
    dummy_packet = bytes([0x0A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x01, 0x00])
    
    try:
        sock.sendto(dummy_packet, (TARGET_IP, TARGET_PORT))
        
        # Antwort empfangen
        data, addr = sock.recvfrom(1024)
        print(f"Antwort erhalten: {data.hex()}")
        
        # Die Bytes an Index 2 und 3 sind die Session ID, die der Master uns zuteilt
        if len(data) >= 4:
            new_id_1 = data[2]
            new_id_2 = data[3]
            print(f"--> GEFUNDEN! Ihre Session ID für dieses Skript ist: {hex(new_id_1)} {hex(new_id_2)}")
            return [new_id_1, new_id_2]
            
    except socket.timeout:
        print("Keine Antwort vom Master. Ist die IP richtig?")
    except Exception as e:
        print(f"Fehler: {e}")
        
    return None

# --- TEST ---
session_id = get_session_id()

if session_id:
    # Ab jetzt nutzen wir diese ID für alle weiteren Befehle (Lauflicht etc.)
    print(f"Nutze ID {session_id} für weitere Kommunikation...")
    # Hier würde jetzt der Loop für das Level-Meter kommen...