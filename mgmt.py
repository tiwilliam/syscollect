import threading
import SocketServer

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

class MGMT:
	def __init__(self, host = '', port = 0):
		self.host = host
		self.port = port

	def start(self, handler = SocketServer.BaseRequestHandler):
		server = ThreadedTCPServer((self.host, self.port), handler)
		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.setDaemon(True)
		server_thread.start()

class MGMTHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request.recv(1024)
		self.request.send(data)
