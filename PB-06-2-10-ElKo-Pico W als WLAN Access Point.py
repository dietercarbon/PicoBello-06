#==========================================================================
#
# PB-6-2-10-ElKo-Pico W als WLAN Access Point_Kom.py
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
import network

# WAP-Betrieb
wap = network.WLAN(network.AP_IF)

# WAP-Konfiguration
wap.config(essid='pico', password='12345678')

# WLAN-Interface aktivieren
wap.active(True)

# Ausgabe der Netzwerk-Konfiguration
print(wap.ifconfig())

"""
Das gegebene Python-Programm zeigt, wie man ein WLAN-Access-Point (WAP) auf einem
Netzwerk einrichten kann. Der Code nutzt die "network" Bibliothek, die in MicroPython
implementiert ist. Hier ist eine detaillierte Erläuterung des Codes:

    import network: Hier wird die "network" Bibliothek importiert, die Funktionen zur Konfiguration
    von Netzwerken in MicroPython bereitstellt.

    wap = network.WLAN(network.AP_IF): Hier wird ein WAP-Objekt erstellt, das mithilfe der
    WLAN-Klasse und dem AP_IF-Attribut initialisiert wird. Das AP_IF-Attribut definiert das
    Objekt als einen WLAN-Access-Point.

    wap.config(essid='pico', password='12345678'): Hier wird die Konfiguration des
    Access-Points vorgenommen. essid (extended service set identifier) ist der Name
    des Netzwerks, den der Access Point sendet, und password ist das Passwort, das zum
    Verbinden mit dem Netzwerk erforderlich ist.

    wap.active(True): Hier wird das WLAN-Interface aktiviert. Das active-Attribut ist
    standardmäßig auf False gesetzt. Durch den Aufruf von active(True) wird das WLAN-Interface
    aktiviert.

    print(wap.ifconfig()): Hier wird die Netzwerkkonfiguration des Access-Points ausgegeben.
    Die Funktion ifconfig() gibt ein Tupel mit vier Elementen zurück, die die IP-Adresse, die
    Subnetzmaske, die Standardgateway-Adresse und die DNS-Server-Adresse des
    Access Points darstellen.

Insgesamt initialisiert und konfiguriert das Programm einen WLAN-Access-Point mit dem
Namen "pico" und dem Passwort "12345678" und gibt die IP-Adresse, die Subnetzmaske,
die Standardgateway-Adresse und die DNS-Server-Adresse des Access-Points aus.





>>> %Run -c $EDITOR_CONTENT
('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8')
>>> 

"""