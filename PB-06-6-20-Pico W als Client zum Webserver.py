#==========================================================================
#
# PB-06-6-20-Pico W als Client zum Webserver.py
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
# Bibliotheken laden
import machine
import network
import rp2
import urequests as requests
import utime as time

# WLAN-Konfiguration
wlanSSID = "pico"
wlanPW = "12345678"
rp2.country('DE')

# Server-URL
serverURL = "http://192.168.4.1"

# Status-LED
led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)

# Funktion: WLAN-Verbindung
def wlanConnect():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WLAN-Verbindung herstellen')
        wlan.active(True)
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            led_onboard.toggle()
            print('.', wlan.status())
            time.sleep(1)
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt')
        led_onboard.on()
        print('WLAN-Status:', wlan.status())
        netConfig = wlan.ifconfig()
        print('IPv4-Adresse:', netConfig[0], '/', netConfig[1])
        print('Standard-Gateway:', netConfig[2])
        print('DNS-Server:', netConfig[3])
    else:
        print('Keine WLAN-Verbindung')
        led_onboard.off()
        print('WLAN-Status:', wlan.status())

# WLAN-Verbindung herstellen
wlanConnect()

# Server-Daten abrufen
try:
    print()
    print('HTTP-Request an', serverURL)
    response = requests.get(serverURL)
    print('Status-Code:', response.status_code)
    if response.status_code == 200:
        # Antwort als Text ausgeben
        print("Antwort vom Server:")
        print(response.text)  # Hier wird die Antwort als Text ausgegeben
    # Verbindung schließen
    response.close()
except OSError:
    print()
    print('Fehler: Keine Netzwerk-Verbindung (WLAN)')
    
# Dieses Programm verbindet einen Raspberry Pi Pico W als Client mit einem WLAN-Netzwerk 
# und sendet einen HTTP-Request an einen Webserver, um die Antwort als Text anzuzeigen.

# 1. Bibliotheken laden:
# Die Bibliotheken "machine", "network", "rp2", "urequests" und "utime" werden importiert, 
# um Hardware und Netzwerkfunktionen zu steuern. "machine" wird zur Steuerung der GPIO-Pins 
# verwendet, "network" ermöglicht die WLAN-Verbindung, "rp2" konfiguriert das Land für die 
# WLAN-Frequenzen, "urequests" dient dem Senden von HTTP-Requests und "utime" bietet Funktionen 
# für Zeitverzögerungen und Timing.

# 2. WLAN-Konfiguration:
# Die Zugangsdaten für das WLAN werden festgelegt. "wlanSSID" und "wlanPW" enthalten die 
# SSID und das Passwort des Netzwerks. Mit "rp2.country('DE')" wird das Land auf Deutschland 
# festgelegt, was wichtig für die Nutzung der WLAN-Kanäle ist.

# 3. Server-URL festlegen:
# Die IP-Adresse des Webservers, von dem der Pico Daten abrufen soll, wird in "serverURL" 
# gespeichert. In diesem Beispiel ist der Webserver unter "192.168.4.1" erreichbar.

# 4. Status-LED konfigurieren:
# Die onboard-LED des Pico wird zur Statusanzeige konfiguriert. Mit "machine.Pin('LED', 
# machine.Pin.OUT, value=0)" wird die LED als Ausgang festgelegt und initial ausgeschaltet.

# 5. Funktion: WLAN-Verbindung herstellen:
# Die Funktion "wlanConnect()" verbindet den Pico mit dem WLAN. 
# Zuerst wird die WLAN-Schnittstelle im Station-Modus (STA) initialisiert, damit der Pico 
# sich mit einem Access Point verbinden kann. Danach wird die Schnittstelle aktiviert und 
# mit den angegebenen Zugangsdaten verbunden. Eine Schleife prüft für maximal 10 Sekunden, 
# ob die Verbindung erfolgreich ist, und blinkt währenddessen die LED. 
# Sobald die Verbindung hergestellt ist, bleibt die LED dauerhaft an, und die Netzwerkdetails 
# (IP-Adresse, Gateway, DNS) werden ausgegeben. Falls die Verbindung fehlschlägt, bleibt die 
# LED ausgeschaltet und der Verbindungsstatus wird ausgegeben.

# 6. WLAN-Verbindung herstellen:
# Hier wird die Funktion "wlanConnect()" aufgerufen, um die WLAN-Verbindung zu starten.

# 7. Server-Daten abrufen:
# Ein HTTP-Request wird an die im Programm definierte URL gesendet. Der Statuscode der Antwort 
# wird überprüft; ein Wert von "200" bedeutet, dass die Anfrage erfolgreich war. Der Textinhalt 
# der Antwort wird dann ausgegeben (z.B. „moin“). Die Verbindung wird anschließend geschlossen, 
# um Ressourcen freizugeben. Im Fehlerfall (z.B. bei fehlender Netzwerkverbindung) gibt das 
# Programm eine entsprechende Meldung aus.

# Zusammenfassend verbindet dieses Programm den Raspberry Pi Pico W mit einem WLAN, stellt eine 
# HTTP-Verbindung zu einem Webserver her und zeigt die Antwort im Terminal an. Während des 
# Verbindungsaufbaus wird der Status durch eine blinkende LED angezeigt. Bei erfolgreicher 
# Verbindung leuchtet die LED dauerhaft, und die empfangene Antwort wird im Terminal ausgegeben.

    
    
    
