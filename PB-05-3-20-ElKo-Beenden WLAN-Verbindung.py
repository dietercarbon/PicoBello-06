#==========================================================================
#
# PB-5-3-20-ElKo-Beenden WLAN-Verbindung.py
#
# (keine Bauteile)
#
#==========================================================================
#
# Bibliotheken laden
import network
import utime as time

# Client-Betrieb
wlan = network.WLAN(network.STA_IF)

# WLAN-Verbindung beenden
if wlan.isconnected():
    wlan.disconnect()
    time.sleep(2)
    print('WLAN-Verbindung beendet')

# WLAN-Verbindungsstatus
print('WLAN-Status:', wlan.status())