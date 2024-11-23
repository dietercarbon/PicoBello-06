#==========================================================================
#
# PB-6-4-10-ElKo-Pico W LED über Webserver schalten.py
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
from DCpriv import DCwlanSSID, DCwlanPW
import machine
import socket
import rp2
import utime as time

# Onboard-LED initialisieren
led = machine.Pin('LED', machine.Pin.OUT)

# WLAN-Konfiguration
wlanSSID = DCwlanSSID()
wlanPW = DCwlanPW()
rp2.country('DE')

# HTML-Datei
html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="shortcut icon" href="data:"><title>Raspberry Pi Pico W</title></head><body><h1 align="center">Hi, I'am your Raspberry Pi Pico W</h1><hr>TEXT<hr><p align="center">DEMO von Elektronik-Kompendium.de</p></body></html>"""

# Funktion: WLAN-Verbindung
def wlanConnect():
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print('WLAN-Verbindung herstellen')
        wlan.active(True)
        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print('.')
            time.sleep(1)
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt')
        netConfig = wlan.ifconfig()
        print('IPv4-Adresse:', netConfig[0])
        print()
        return netConfig[0]
    else:
        print('Keine WLAN-Verbindung')
        print('WLAN-Status:', wlan.status())
        print()
        return ''

# WLAN-Verbindung herstellen
ipv4 = wlanConnect()

# HTTP-Server starten
if ipv4 != '':
    print('Server starten')
    addr = socket.getaddrinfo(ipv4, 80)[0][-1]
    server = socket.socket()
    server.bind(addr)
    server.listen(1)
    print('Server hört auf', addr)
    print()
    print('Beenden mit STRG + C')
    print()

# Auf eingehende Verbindungen hören
while True:
    try:
        conn, addr = server.accept()
        print('HTTP-Request von Client', addr)
        request = conn.recv(1024)
        #print('Request:', request)
        request = str(request)
        request = request.split()
        print('URL:', request[1])
        # URL auswerten
        if request[1] == '/light/on':
            print('LED einschalten')
            led.value(1)
        elif request[1] == '/light/off':
            print('LED ausschalten')
            led.value(0)
        elif request[1] == '/light/toggle':
            print('LED umschalten')
            led.toggle()
        # LED-Status auswerten
        #print('LED-Status:', led.value())
        state_is = ''
        if led.value() == 1:
            state_is += '<p align="center"><b>LED ist AN</b> <a href="/light/off"><button>AUS</button></a></p>'
        if led.value() == 0:
            state_is += '<p align="center"><b>LED ist AUS</b> <a href="/light/on"><button>AN</button></a></p>'
        # HTTP-Response erzeugen und senden
        response = html.replace('TEXT', state_is)
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
        print('HTTP-Response gesendet')
        print()
    except OSError as e:
        break
    except (KeyboardInterrupt):
        break

try: conn.close()
except NameError: pass
try: server.close()
except NameError: pass
print('Server beendet')

"""
Das vorliegende Micropython-Programm für den Raspberry Pi Pico implementiert
einen HTTP-Server, der über WLAN erreichbar ist und es ermöglicht, die
angeschlossene LED des Pico-Boards ein- und auszuschalten sowie den Status
der LED abzufragen. Der Programmcode kann in vier Abschnitte unterteilt werden:

    Bibliotheken und Variablen initialisieren
    WLAN-Verbindung herstellen
    HTTP-Server starten
    Auf eingehende Verbindungen hören

Zu Beginn des Programms werden notwendige Bibliotheken wie DCpriv, machine,
socket und rp2 geladen. Darüber hinaus wird die Standardbibliothek utime
unter dem Alias "time" importiert. Es folgt die Initialisierung der
Onboard-LED, die als Ausgangsport definiert wird.

Anschließend wird die WLAN-Konfiguration durchgeführt. Dazu werden die
WLAN-SSID und das WLAN-Passwort aus der externen Datei DCpriv.py ausgelesen.
Zudem wird die Länderkennung auf "DE" gesetzt, um die WLAN-Verbindung auf die
Frequenzen in Deutschland einzustellen.

Die HTML-Seite wird als Zeichenkette definiert, die später als Antwort auf
HTTP-Anfragen gesendet wird. Dabei wird der Platzhalter "TEXT" durch den
aktuellen Zustand der LED ersetzt.

Die Funktion "wlanConnect()" wird definiert, um eine WLAN-Verbindung
herzustellen. Dazu wird die Bibliothek "network" importiert und ein neues
WLAN-Objekt erstellt. Wenn keine Verbindung besteht, wird versucht, eine
Verbindung herzustellen. Dabei wird eine Schleife durchlaufen, die alle
1 Sekunde prüft, ob eine Verbindung hergestellt wurde. Wenn dies der Fall
ist, wird die IPv4-Adresse ausgegeben und zurückgegeben. Wenn keine Verbindung
hergestellt werden kann, wird eine leere Zeichenkette zurückgegeben.

Der HTTP-Server wird gestartet, wenn eine WLAN-Verbindung hergestellt werden
konnte. Dazu wird die IP-Adresse des Pico-Boards ermittelt und ein Socket-Objekt
erstellt, das auf eingehende Verbindungen lauscht. Es wird auf eingehende
Verbindungen gewartet, während der Server in einer Endlosschleife ausgeführt wird.

Wenn eine HTTP-Anfrage empfangen wird, wird diese analysiert und die
entsprechende Aktion ausgeführt. Wenn die URL "/light/on" aufgerufen wird,
wird die LED eingeschaltet. Wenn die URL "/light/off" aufgerufen wird, wird
die LED ausgeschaltet. Wenn die URL "/light/toggle" aufgerufen wird, wird
der LED-Zustand umgeschaltet. Der aktuelle Zustand der LED wird dann in der
HTML-Seite aktualisiert und als HTTP-Antwort zurückgesendet.

Das Programm wird durch eine Ausnahmebehandlung beendet, wenn entweder eine
OSError-Ausnahme auftritt oder die Ausführung durch das Drücken von STRG + C
abgebrochen wird. Dabei werden der Socket und die Verbindung geschlossen,
wenn sie existieren. Am Ende des Programms wird eine Nachricht ausgegeben,
die den erfolgreichen Abschluss des Programms signalisiert.

Insgesamt ist das Programm gut strukturiert und einfach zu verstehen.
Die Kommentare im Code sind hilfreich, um die Funktionsweise des Programms
zu verstehen.





>>> %Run -c $EDITOR_CONTENT
WLAN-Verbindung herstellen
.
.
.
.
WLAN-Verbindung hergestellt
IPv4-Adresse: 192.168.0.221

Server starten
Server hört auf ('192.168.0.221', 80)

Beenden mit STRG + C

HTTP-Request von Client ('192.168.0.101', 57281)
URL: /light/on
LED einschalten
HTTP-Response gesendet

HTTP-Request von Client ('192.168.0.101', 57282)
URL: /light/off
LED ausschalten
HTTP-Response gesendet

HTTP-Request von Client ('192.168.0.101', 57283)
URL: /light/off
LED ausschalten
HTTP-Response gesendet

HTTP-Request von Client ('192.168.0.101', 57284)
URL: /light/on
LED einschalten
HTTP-Response gesendet

HTTP-Request von Client ('192.168.0.101', 57285)
URL: /light/on
LED einschalten
HTTP-Response gesendet

Server beendet
>>> 
"""