# -*- coding: utf-8 -*-
# vim:set ts=8 sts=8 sw=8 tw=80 noet cc=80:

import sleekxmpp
import logging

log = logging.getLogger(__name__)

class Client(sleekxmpp.ClientXMPP):
	mentation_listeners = []
	message_listeners = []
	online_listeners = []
	participants = {}

	def __init__(self, jid, password, room, nick):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)

		self.room = room
		self.nick = nick

		self.add_event_handler("session_start", self.start)
		self.add_event_handler("groupchat_message", self.muc_message)
		self.add_event_handler("message", self.message)
		self.add_event_handler("muc::%s::got_online" % self.room,
				self.muc_online)
		self.add_event_handler("muc::%s::got_offline" % self.room,
				self.muc_offline)

	def add_mentation_listener(self, listener):
		self.mentation_listeners += [ listener ]

	def add_message_listener(self, listener):
		self.message_listeners += [ listener ]

	def add_online_listener(self, listener):
		self.online_listeners += [ listener ]

	def start(self, event):
		self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

	def muc_message(self, msg):
		nick = msg['mucnick']
		if nick != self.nick:
			if msg['body'].startswith(self.nick):
				if len(msg['body']) <= len(self.nick) + 2:
					return
				text = msg['body'][len(self.nick) + 1:].strip()
				for listener in self.mentation_listeners:
					if listener(text, nick,
							self.send_message):
						break
			else:
				for listener in self.message_listeners:
					if listener(msg['body'], nick,
							self.send_message):
						break

	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			text = msg['body']
			nick = None
			for listener in self.mentation_listeners:
				if listener(text, nick, self.send_message):
					break
			#msg.reply("Thanks for sending\n%(body)s" % msg).send()

	def muc_online(self, presence):
		if presence['muc']['nick'] != self.nick:
			jid = presence['from'].full
			role = presence['muc']['role']
			nick = presence['muc']['nick']
			affiliation = presence['muc']['affiliation']
			self.participants[jid] = {'jid': jid,
					'role': role,
					'nick': nick,
					'affiliation': affiliation}
			log.info("%s: %s [%s]" % (jid, role, nick))
			for listener in self.online_listeners:
				listener(nick, role, self.send_message)

	def muc_offline(self, presence):
		if presence['muc']['nick'] != self.nick:
			jid = presence['from'].full
			del self.participants[jid]

	def send_message(self, msg):
		sleekxmpp.ClientXMPP.send_message(self, mto=self.room,
				mbody=msg, mtype='groupchat')

	def set_role(self, nick, role):
		log.info("setting role for %s to %s" % (nick, role))
		self.plugin['xep_0045'].setRole(self.room, nick, role)
