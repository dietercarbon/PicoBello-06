#==========================================================================
#
# PB-6-2-20-ElKo-Pico W als WLAN Access Point Funktion.py
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
import network
import rp2

# Funktion: WAP erstellen
def wapCreate():
    # WAP-Konfiguration
    rp2.country('DE')
    wap = network.WLAN(network.AP_IF)
    wap.config(essid='pico', password='12345678')
    wap.active(True)
    # Ausgabe der Netzwerk-Konfiguration
    netConfig = wap.ifconfig()
    print('IPv4-Adresse:', netConfig[0], '/', netConfig[1])
    print('Standard-Gateway:', netConfig[2])
    print('DNS-Server:', netConfig[3])

# WAP erstellen
wapCreate()

"""
Dieses Micropython-Programm erstellt ein Wireless Access Point (WAP) auf dem
Raspberry Pi Pico. Dazu werden die Bibliotheken "network" und "rp2" geladen.

In der Funktion "wapCreate()" wird zunächst die WLAN-Landeskonfiguration auf
"DE" gesetzt und anschließend ein neues WLAN-Objekt mit dem Access Point
Interface (AP_IF) erstellt. Das WLAN-Objekt wird dann mit den
Konfigurationsparametern ESSID (Name des Netzwerks) und Passwort konfiguriert
und aktiviert.

Die Netzwerkkonfiguration wird dann mit der Methode "ifconfig()" abgerufen
und in der Konsole ausgegeben.

Das Programm endet mit dem Aufruf der Funktion "wapCreate()", die den WAP
erstellt und dessen Netzwerkkonfiguration ausgibt.

Die Erstellung eines WAPs auf einem Raspberry Pi Pico ist nützlich, um andere
Geräte (z.B. Smartphones oder Laptops) mit dem Pico zu verbinden, um Daten
auszutauschen oder um eine Verbindung zum Internet herzustellen, wenn der
Pico selbst über einen Internetzugang verfügt.






>>> %Run -c $EDITOR_CONTENT
IPv4-Adresse: 192.168.4.1 / 255.255.255.0
Standard-Gateway: 192.168.4.1
DNS-Server: 8.8.8.8
>>> 

"""