import network
import socket
import time
import machine

# WLAN-Client Setup
ssid = "Pico-AP"
password = "12345678"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Verbindet mit WLAN...")
    time.sleep(1)

print("Verbunden mit IP:", wlan.ifconfig()[0])

# Onboard-Taster Setup
taster = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Server IP und Port (vom AP)
server_ip = "192.168.4.1"
server_port = 80

# Variable, die den Zustand speichert
led_status = "LED_OFF"

try:
    while True:
        # Prüfen, ob der Taster gedrückt ist
        if taster.value() == 1:
            # Zustand umschalten
            if led_status == "LED_OFF":
                led_status = "LED_ON"
            else:
                led_status = "LED_OFF"

            try:
                # Verbindung zum AP herstellen und Nachricht senden
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                client_socket.send(led_status.encode())
                client_socket.close()
                print("Nachricht gesendet:", led_status)
            except Exception as e:
                print("Fehler beim Senden der Nachricht:", e)

            # Entprellung
            time.sleep(0.5)

except KeyboardInterrupt:
    wlan.disconnect()
