import socket

ip = "192.168.0.19"
port = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1) # Nur 1 Sekunde warten
result = sock.connect_ex((ip, port))

if result == 0:
    print(f"Port {port} ist OFFEN! Modbus sollte gehen.")
else:
    print(f"Port {port} ist GESCHLOSSEN. (Code: {result})")

sock.close()