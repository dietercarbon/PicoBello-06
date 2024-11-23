#==========================================================================
#
# PB-6-5-10-ElKo-Pico W WLAN-Stoppuhr.pyw
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
from machine import Pin, Timer
import network
import socket
import rp2
import utime as time
import tm1637
from DCpriv import DCwlanSSID, DCwlanPW


# Konfiguration: WLAN-Zugang
WIFI_SSID = DCwlanSSID()
WIFI_PASSWORD = DCwlanPW()
rp2.country('DE')

# Display TM1637 initialisieren
display = tm1637.TM1637(clk=Pin(21), dio=Pin(20))

# Funktion: Ausgabe auf dem Display
def outputDisplay(counter, points):
    # Zähler in Minuten und Sekunden umrechnen und anzeigen
    timeValue = time.localtime(counter)
    secs = timeValue[5]
    if counter >= 3600: mins = int(counter/60)
    else: mins = timeValue[4]
    display.numbers(mins, secs, points)

# Funktion: Herunterzählen und zeitabhängige Bedingungen
def count(value):
    global counter
    global points
    global run
    # Blinkender Doppelpunkt im Wechsel
    if points == 0: points = 1
    else: points = 0
    # Zähler erhöhen
    counter += 1
    # höchster darstellbarer Wert erreicht
    if counter == 5940:
        clock.deinit()
        run = 0
        points = 1
        print('Ende')
    # Ausgabe auf dem Display
    outputDisplay(counter, points)

# Funktion: WLAN-Verbindung
def connectWLAN():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WLAN-Verbindung herstellen')
        wlan.config(pm = 0xa11140)
        wlan.active(True)
        #wlan.connect(wlanSSID, wlanPW)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3: break
            print('.')
            time.sleep(1)
    # WLAN-Verbindung prüfen
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt / WLAN-Status:', wlan.status())
        ipconfig = wlan.ifconfig()
        #print('IPv4-Adresse:', ipconfig[0])
    else:
        print('WLAN-Status:', wlan.status())
        raise RuntimeError('Keine WLAN-Verbindung')
    print()
    # IP-Adresse zurückgeben
    return ipconfig[0]

# Funktion: Webserver
def openSocket(ip):
    print('Server starten')
    address = (ip, 80)
    server = socket.socket()
    server.bind(address)
    server.listen(1)
    print('Server hört auf', ip)
    print('Beenden mit STRG + C')
    print()
    return server

# Funktion: HTML-Seite erzeugen
def getHTML(counter, run):
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="shortcut icon" href="data:"><title>Stoppuhr - Raspberry Pi Pico W</title></head><body><h1>Stoppuhr</h1>"""
    if run == 0:
        html += """<p><a href="/toggle"><button>STARTEN</button></a></p>"""
        if counter > 0:
            html += """<p><a href="/reset"><button>Zurücksetzen</button></a></p>"""
    else:
        html += """<p><a href="/toggle"><button>STOPPEN</button></a></p>"""
    html += """</body></html>"""
    return str(html)

# Funktion: Webserver-Verbindungen
def webserver(server):
    global counter
    global run
    while True:
        try:
            client, addr = server.accept()
            #print('HTTP-Request von Client', addr)
            request = client.recv(1024)
            #print('Request:', request)
            request = str(request)
            try: url = request.split()[1]
            except IndexError: url = '/'
            #print('URL:', url)
            if url == '/toggle':
                if run == 1:
                    clock.deinit()
                    run = 0
                    outputDisplay(counter, 1)
                    print('Stop')
                else:
                    clock.init(freq=1, mode=Timer.PERIODIC, callback=count)
                    run = 1
                    print('Start')
            elif url == '/reset':
                counter = 0
                outputDisplay(counter, 1)
                print('Reset')
            elif url == '/':
                print('Startseite')
            else:
                print('Unbekannte URL:', url)
            response = getHTML(counter, run)
            client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            client.send(response)
            client.close()
            #print('HTTP-Response gesendet')
            print()
        except OSError as e:
            break
        except (KeyboardInterrupt):
            break
    # Client-Verbindung und Server beenden
    try: client.close()
    except NameError: pass
    try: server.close()
    except NameError: pass
    print('Server beendet')

# Hauptprogramm

# Startwert der Stoppuhr
counter = 0

# Countdown läuft (1) / läuft nicht (0)
run = 0

# Doppelpunkt
points = 1

# Initialisierung Timer für Countdown
clock = Timer()

# Ausgabe auf dem Display
outputDisplay(counter, points)

try:
    ip = connectWLAN()
    server = openSocket(ip)
    webserver(server)
except KeyboardInterrupt:
    machine.reset()
    
"""
Das vorliegende Programm ist eine Stoppuhr, die auf dem Raspberry Pi Pico
ausgeführt wird. Der Benutzer kann die Stoppuhr starten, stoppen und
zurücksetzen, indem er eine HTML-Seite aufruft, die auf einem lokalen
Webserver gehostet wird. Die aktuelle Zeit wird auf einem TM1637-Display
angezeigt.

Der Code beginnt mit dem Laden der erforderlichen Bibliotheken, einschließlich
machine, network, socket, rp2, utime und tm1637. In diesem Abschnitt werden
auch die WLAN-Zugangsdaten für die Verbindung zum Netzwerk konfiguriert.

Das TM1637-Display wird dann initialisiert und es werden Funktionen für die
Ausgabe auf dem Display und für das Herunterzählen und zeitabhängige Bedingungen
definiert. Die Funktion outputDisplay konvertiert den Zähler in Minuten und
Sekunden und zeigt diese auf dem Display an. Die Funktion count erhöht den
Zähler, wechselt den blinkenden Doppelpunkt im Wechsel und überprüft, ob
der höchste darstellbare Wert erreicht wurde. Wenn dies der Fall ist, wird
der Timer deinitialisiert, das Programm wird beendet und "Ende" wird ausgegeben.

Es gibt auch eine Funktion für die WLAN-Verbindung, die die Verbindung zum
Netzwerk herstellt und die IP-Adresse des Picos zurückgibt.

Die Funktion openSocket initialisiert einen Socket, der auf eingehende
Verbindungen lauscht. Die Funktion getHTML erzeugt eine HTML-Seite, die den
aktuellen Zählerstand und Schaltflächen zum Starten, Stoppen und Zurücksetzen
der Stoppuhr enthält. Die Funktion webserver behandelt eingehende HTTP-Anfragen
von Clients und führt die entsprechenden Aktionen aus, um die Stoppuhr zu
starten, zu stoppen oder zurückzusetzen.

Wenn der Benutzer die Stoppuhr startet, wird der Timer initialisiert und
die count-Funktion wird periodisch aufgerufen, um den Zähler um 1 zu erhöhen
und den Wert auf dem Display anzuzeigen. Wenn der Benutzer die Stoppuhr stoppt,
wird der Timer deinitialisiert und der Zählerstand wird angezeigt. Wenn der
Benutzer die Stoppuhr zurücksetzt, wird der Zähler auf Null gesetzt und angezeigt.

Insgesamt ist dies ein gut strukturiertes Programm, das eine einfache Stoppuhr
implementiert und auf einem Webserver gehostet wird, um die Interaktion mit
dem Benutzer zu ermöglichen. Das Programm nutzt auch die Funktionen des
TM1637-Displays, um den aktuellen Zählerstand auf einfache Weise anzuzeigen.













>>> %Run -c $EDITOR_CONTENT
WLAN-Verbindung herstellen
.
.
.
.
WLAN-Verbindung hergestellt / WLAN-Status: 3

Server starten
Server hört auf 192.168.0.222
Beenden mit STRG + C

Start

Stop

Start

Stop

Reset

Server beendet
>>> 


"""