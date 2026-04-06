import requests
import time
import struct
import datetime

# ------------------------------------------------------------------
# KONFIGURATION
# ------------------------------------------------------------------
MASTER_IP = "192.168.0.19"
URL = f"http://{MASTER_IP}/ports.jsn"

# Intervall in Sekunden
POLL_INTERVAL = 1.0

# ------------------------------------------------------------------
# PARSER-LOGIK
# ------------------------------------------------------------------
def parse_bcm_hex(hex_str):
    """
    Nimmt den Hex-String (mit Leerzeichen) und wandelt ihn in eine Liste von Floats um.
    Ein BCM Sensor liefert meistens mehrere 4-Byte Floats hintereinander.
    """
    # 1. Leerzeichen entfernen
    clean = hex_str.replace(" ", "").strip()
    
    # 2. In Bytes umwandeln
    try:
        raw_bytes = bytes.fromhex(clean)
    except ValueError:
        return []

    values = []
    
    # 3. In 4-Byte Häppchen schneiden und als Float interpretieren
    # Wir schauen uns die ersten 5 Werte an (20 Bytes)
    # Format '>f' bedeutet: Big-Endian Float (Standard für IO-Link)
    for i in range(0, len(raw_bytes), 4):
        if i + 4 > len(raw_bytes):
            break
            
        chunk = raw_bytes[i:i+4]
        try:
            # struct.unpack gibt ein Tuple zurück, wir brauchen das erste Element
            val = struct.unpack('>f', chunk)[0]
            values.append(val)
        except:
            values.append(0.0)
            
    return values

# ------------------------------------------------------------------
# HAUPTSCHLEIFE
# ------------------------------------------------------------------
print(f"Verbinde zu {MASTER_IP}...")

try:
    while True:
        try:
            t_start = time.time()
            resp = requests.get(URL, timeout=1.0)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # Suchen nach dem BCM Sensor in der Port-Liste
                bcm_port = None
                for p in data.get("ports", []):
                    # Sicherheitscheck: Hat der Port überhaupt Inputs?
                    if "BCM" in p.get("productName", ""):
                        bcm_port = p
                        break
                
                if bcm_port:
                    raw_hex = bcm_port.get("processInputs", "")
                    
                    # Parsen
                    messwerte = parse_bcm_hex(raw_hex)
                    
                    # --- AUSGABE ---
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"[{timestamp}] Sensor an Port {bcm_port.get('id', '?')}")
                    
                    if len(messwerte) >= 4:
                        # Zuweisung basierend auf typischem BCM Mapping (kann variieren!)
                        # Oft: v-RMS (X/Y/Z) oder v-Peak, dann Temperatur
                        
                        val1 = messwerte[0] # Vibration 1 (z.B. v-RMS)
                        val2 = messwerte[1] # Vibration 2
                        val3 = messwerte[2] # Vibration 3
                        val4 = messwerte[3] # Temperatur (oft an Stelle 4)
                        
                        print(f"  ├─ Vibration A: {val1:.4f}")
                        print(f"  ├─ Vibration B: {val2:.4f}")
                        print(f"  ├─ Vibration C: {val3:.4f}")
                        print(f"  └─ Temperatur?: {val4:.2f} °C") # Testen durch Anhauchen!
                        print("-" * 30)
                    else:
                        print(f"  Rohdaten (zu kurz): {raw_hex}")
                        
                else:
                    print("Kein BCM Sensor gefunden.")
            
            else:
                print(f"Fehler HTTP {resp.status_code}")

        except requests.exceptions.Timeout:
            print("Timeout...")
        except Exception as e:
            print(f"Fehler: {e}")

        # Pause bis zum nächsten Takt
        time.sleep(POLL_INTERVAL)

except KeyboardInterrupt:
    print("\nBeende Skript.")