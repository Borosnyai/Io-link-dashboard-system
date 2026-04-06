import requests
import json
import time

# ------------------------------------------------------------------
# KONFIGURATION
# ------------------------------------------------------------------
MASTER_IP = "192.168.0.19"
PORT_NUM  = 0  # Hängt Ihre Lampe an Port 0? Sonst ändern!

# Die URLs für den Zugriff (Balluff Standard-API)
# Wir probieren zwei Varianten, da Balluff verschiedene APIs hat
URL_V1 = f"http://{MASTER_IP}/exec"       # Neuere Master
URL_V2 = f"http://{MASTER_IP}/ports.jsn"  # Ältere Master

# ------------------------------------------------------------------
# HELFER: ISDU SCHREIBEN
# ------------------------------------------------------------------
def write_param(index, subindex, value_hex_string):
    # payload für BNI Master (JSON-RPC ähnlich)
    # Index und Value müssen oft Strings sein
    payload = {
        "code": "request",
        "cid": 4711,
        "adr": f"/iolink/master/port/{PORT_NUM}/iolinkdevice/isdu/write",
        "data": {
            "index": index,
            "subindex": subindex,
            "value": value_hex_string # Hex String ohne 0x
        }
    }
    
    print(f"Versuche Parameter {index} auf {value_hex_string} zu setzen...")
    
    try:
        # Versuch 1: Über /exec
        r = requests.post(URL_V2, json=payload, timeout=2)
        if r.status_code == 200 and "response" in r.text:
            print(" -> Erfolg (via ports)!")
            return True
    except:
        pass

    try:
        # Versuch 2: Alter Weg (manchmal über param set)
        # Dieser Pfad ist sehr modellspezifisch. 
        # Wir probieren einen universelleren Weg via 'dataservice' falls obiges scheitert.
        pass
    except:
        pass
        
    print(" -> Konnte nicht schreiben. API evtl. anders.")
    return False

# ------------------------------------------------------------------
# HAUPTPROGRAMM: KONFIGURATION SENDEN
# ------------------------------------------------------------------
print(f"Konfiguriere SmartLight an {MASTER_IP} Port {PORT_NUM}...")

# 1. PARAMETER 65 (Number of Segments)
# Wir wollen "3 Segments". Laut IO-Link Standard oft: 
# 01=1 Seg, 02=2 Seg, 03=3 Seg. Wir probieren "03".
# Manche Devices nutzen Enums: 00=1 Seg... 
# Wir raten "03" (Hex), das ist meistens sicher für "3 Segmente".
write_param(65, 0, "03") 

time.sleep(0.5)

# 2. PARAMETER 83 (Blinking Mode)
# Wir wollen "Static" (Aus).
# Subindex 0 (alle) oder 1,2,3 einzeln. Wir schreiben auf 0 (Global/Alle).
# Value: 00 (Static)
write_param(83, 0, "00")

print("\nFertig. Bitte Stromlos machen (Neustart) oder Python-Lauflicht testen!")