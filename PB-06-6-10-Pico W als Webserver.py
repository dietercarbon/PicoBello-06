#==========================================================================
#
# PB-6-3-10-ElKo-Pico W als Webserver.py
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
import socket
import utime as time

# HTML
html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="shortcut icon" href="data:"><title>Raspberry Pi Pico</title></head><body><h1 align="center">Raspberry Pi Pico W</h1><p align="center">Verbindung mit %s</p></body></html>"""

# HTTP-Server starten
print('Server starten')
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
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
        # HTTP-Request anzeigen
        print('Request:', request)
        # HTTP-Response senden
        response = html % str(addr)
        conn.send("HTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        #conn.send(response)
        conn.send("moin-moin")
        conn.send("moin-moin-moin")
        conn.close()
        print('HTTP-Response gesendet')
        print()
    except OSError as e:
        break
    except (KeyboardInterrupt):
        break

try: conn.close()
except NameError: pass
server.close()
print('Server beendet')

"""
Das vorliegende Micropythonprogramm ist ein HTTP-Server, der auf dem
Raspberry Pi Pico ausgeführt werden kann. Der Server empfängt eingehende
HTTP-Anforderungen von Clients und sendet eine HTTP-Antwort zurück, die
eine einfache HTML-Seite mit einer Meldung über die erfolgreiche Verbindung
mit dem Client enthält. Das Programm nutzt die Bibliotheken "socket" und "utime".

Der Code beginnt damit, die Bibliotheken "socket" und "utime" zu importieren.
Anschließend wird eine HTML-Seite definiert, die später als Antwort auf die
HTTP-Anforderungen der Clients gesendet wird.

Danach startet der HTTP-Server. Der Server wird auf allen Schnittstellen des
Geräts gestartet (durch die Verwendung von '0.0.0.0' als IP-Adresse) und horcht
auf Port 80. Der Server bindet an die Adresse und hört auf eingehende Verbindungen.

In der Schleife wartet der Server auf eingehende Verbindungen. Wenn eine
Verbindung eingeht, wird die HTTP-Anforderung vom Client empfangen und
angezeigt. Dann wird eine HTTP-Antwort generiert, die die zuvor definierte
HTML-Seite enthält, und an den Client zurückgesendet. Schließlich wird die
Verbindung geschlossen und eine Meldung wird ausgegeben, dass die HTTP-Antwort
gesendet wurde.

Wenn eine Ausnahme auftritt, z.B. wenn das Programm mit "STRG + C" beendet
wird, werden die Verbindungen geschlossen und der Server wird beendet.

Insgesamt ist dies ein einfaches Beispiel für einen HTTP-Server, der auf
dem Raspberry Pi Pico ausgeführt werden kann. Es demonstriert die Verwendung
der "socket" Bibliothek, um eingehende Verbindungen zu empfangen und eine
Antwort zu senden. Der Code ist einfach zu verstehen und zu modifizieren,
um eigene Anforderungen zu erfüllen.








>>> %Run -c $EDITOR_CONTENT
Server starten
Server hört auf ('0.0.0.0', 80)

Beenden mit STRG + C

Beenden mit STRG + C

HTTP-Request von Client ('192.168.4.17', 51791)
Request: b'GET / HTTP/1.1\r\nHost: 192.168.4.1\r\nUpgrade-Insecure-Requests:
1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*
/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X)
AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/
604.1\r\nAccept-Language: de-DE,de;q=0.9\r\nAccept-Encoding: gzip, deflate
\r\nConnection: keep-alive\r\n\r\n'
HTTP-Response gesendet

HTTP-Request von Client ('192.168.4.17', 51792)
Request: b'GET / HTTP/1.1\r\nHost: 192.168.4.1\r\nUpgrade-Insecure-Requests:
1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*
/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X)
AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/
604.1\r\nAccept-Language: de-DE,de;q=0.9\r\nAccept-Encoding: gzip, deflate
\r\nConnection: keep-alive\r\n\r\n'
HTTP-Response gesendet


"""
