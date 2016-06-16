# -*- coding: utf-8 -*-
# vim:set ts=8 sts=8 sw=8 tw=80 noet cc=80:

import requests
import re
from lxml import etree
from io import StringIO
from module import Module, PRIVMSG, MUC

# extend 'Module' to get all the useful functions
class Weather(Module):
	def __init__(self, **keywords):
		# register for private messages only
		super(Weather, self).__init__([PRIVMSG,MUC], name=__name__,
				**keywords)

	def get_weather(self):
		try:
			response = requests.get('http://www.meteo.physik.uni-muenchen.de/dokuwiki/doku.php?id=wetter:garching:neu')
			html = str(response.content)
			parser = etree.HTMLParser()
			tree = etree.parse(StringIO(html), parser)

			#dictionary/array
			values = [ re.sub(r'\s+', ' ', x.strip()) for x in tree.xpath('//table[@border="1"]/tr/td/text()') ]

			return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
					(values[3], values[12], values[39], values[48])
		except Exception as e:
			# there is a central logging infrastructure
			self.do_log("Exception caught: %s" % str(e))

	# override the callback method to handle incoming messages
	        def get_hoehe(self, hoehe):
                try:
                        response = requests.get('http://www.meteo.physik.uni-muenchen.de/dokuwiki/doku.php?id=wetter:garching:neu')
                        html = str(response.content)
                        parser = etree.HTMLParser()
                        tree = etree.parse(StringIO(html), parser)

                        #dictionary/array
                        values = [ re.sub(r'\s+', ' ', x.strip()) for x in tree.xpath('//table[@border="1"]/tr/td/text()') ]

                        if hoehe == "0.2":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[0], values[9], values[36], values[45])
                        elif hoehe == "0.5":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[1], values[10], values[37], values[46])
                        elif hoehe == "1" or hoehe == "1.0" or hoehe == "1.0m" or hoehe == "1m" :
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[2], values[11], values[38], values[47])
                        elif hoehe == "2" or hoehe == "2.0":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[3], values[12], values[39], values[48])
                        elif hoehe == "5" or hoehe == "5.0":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[4], values[13], values[40], values[49])
                        elif hoehe == "10" or hoehe == "10.0":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[5], values[14], values[41], values[50])
                        elif hoehe == "20" or hoehe == "20.0":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[6], values[15], values[42], values[51])
                        elif hoehe == "35" or hoehe == "35.0":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[7], values[16], values[43], values[52])
                        elif hoehe == "50" or hoehe == "50.0":
                                return "Es hat auf %s, %s bei %s Luftfeuchtigkeit und die Windgeschwindigkeit beträgt %s" % \
                                        (values[8], values[17], values[44], values[53])
                        else:
                                return "Error: Deine Eingegebene Zahl passt nich. Erlaubt ist alles in Form 'wetter', 'wetter 1', 'wetter 1.0', 'wetter 0.5'"
                except Exception as e:
                        # there is a central logging infrastructure
                        self.do_log("Exception caught: %s" % str(e))

        # override the callback method to handle incoming messages
        def private_msg(self, jid, msg):
                if msg == "weather" or msg == "wetter": # if someone sent 'weather'...
                        weather = self.get_weather()
                        self.send_private(jid, weather) # ... send the weather
                elif msg.startswith("weather "):
                        hoehe = msg[8:].strip()
                        self.send_private(jid, hoehe) # ... send the weather
                        weather = self.get_hoehe(hoehe)
                        self.send_private(jid, "Dein Wetter:") # ... send the weather
                        self.send_private(jid, weather) # ... send the weather
                elif msg == "weather help" or msg == "wetter help":
                        self.send_private(jid, "Mögliches Ansprechen:\n
                                Daten die Ausgegeben werden: Höhe des Messpunktes, Temperatur, Prozentuale Luftfeuchtigkeit, Windgeschwindigkeit in m/s
                                'wetter' - Dann sieht man die Aktuellen Daten auf 2m Höhe.
                                'wetter 0.5' - Daten von 0.5m Höhe
                                'wetter 1' - Daten von 1m Höhe
                                Erlaubte Höhen sind: '0.2, 0.5, 1, 1.0, 2, 2.0, 5, 5.0, 10, 10.0 20, 20.0, 35, 35.0, 50, 50.0'
                                Einen schönen Tag wünsche ich!
                                Dein Wetter-Orakel vom LRZ")
                elif msg.startswith("wetter "):
                        hoehe = msg[7:].strip()
                        self.send_private(jid, hoehe) # ... send the weather
                        weather = self.get_hoehe(hoehe)
                        self.send_private(jid, "Dein Wetter:") # ... send the weather
                        self.send_private(jid, weather) # ... send the weather
        def muc_msg(self, msg, nick, **keywords):
                if msg == "weather" or msg == "wetter": # if someone sent 'weather
#                       self.send_muc("Ich höre dich")
                        weather = self.get_weather()
                        self.send_muc(weather)
                elif msg.startswith("weather "):
                        hoehe = msg[8:].strip()
                        weather = self.get_hoehe(hoehe)
                        self.send_muc(weather)
                elif msg == "weather help" or msg == "wetter help":
                        self.send_muc("Mögliches Ansprechen: \n
                                Daten die Ausgegeben werden: Höhe des Messpunktes, Temperatur, Prozentuale Luftfeuchtigkeit, Windgeschwindigkeit in m/s \n
                                'wetter' - Dann sieht man die Aktuellen Daten auf 2m Höhe. \n
                                'wetter 0.5' - Daten von 0.5m Höhe\n
                                'wetter 1' - Daten von 1m Höhe \n
                                Elaubte Höhen sind: '0.2, 0.5, 1, 1.0, 2, 2.0, 5, 5.0, 10, 10.0 20, 20.0, 35, 35.0, 50, 50.0'\n
                                Einen schönen Tag wünsche ich!\n
                                Dein Wetter-Orakel vom LRZ")
                elif msg.startswith("wetter "):
                        hoehe = msg[7:].strip()
                        weather = self.get_hoehe(hoehe)
                        self.send_muc(weather)

