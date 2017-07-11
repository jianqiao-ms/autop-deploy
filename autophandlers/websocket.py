#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from tornado.websocket import WebSocketHandler

liveWebSockets = set()
def webSocketSendMessage(message):
    removable = set()
    for ws in liveWebSockets:
        if not ws.ws_connection or not ws.ws_connection.stream.socket:
            removable.add(ws)
        else:
            ws.write_message(message)
    for ws in removable:
        liveWebSockets.remove(ws)

class MsgSocket(WebSocketHandler, object):
    def check_origin(self, origin):
        return True

    def open(self):
        liveWebSockets.add(self)
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")