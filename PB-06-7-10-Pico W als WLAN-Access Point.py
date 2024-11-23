import network
import socket
import machine

# WLAN Access Point Setup
ssid = "Pico-AP"
password = "12345678"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

while not ap.active():
    pass

print("Access Point aktiv mit IP:", ap.ifconfig()[0])

# Onboard-LED Setup
led = machine.Pin("LED", machine.Pin.OUT)

# Socket Setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 80))
server_socket.listen(1)

try:
    while True:
        print("Warten auf Verbindung...")
        conn, addr = server_socket.accept()
        print(f"Verbindung von {addr}")

        # Daten empfangen
        data = conn.recv(1024).decode()
        print("Empfangene Daten:", data)

        # LED steuern basierend auf der Nachricht
        if data == "LED_ON":
            led.value(1)
        elif data == "LED_OFF":
            led.value(0)

        conn.close()

except KeyboardInterrupt:
    server_socket.close()

