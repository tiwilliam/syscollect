import logging
import SocketServer

import static

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	allow_reuse_address = 1

	def __init__(self, server_address, request_handler_class):
		SocketServer.TCPServer.__init__(self, server_address, request_handler_class)

		self.cmds = []
		self.logger = logging.getLogger('default')

	def serve(self):
		try:
			self.serve_forever()
		except:
			self.shutdown()

	def add_callback(self, cmd, callback):
		self.cmds += [(cmd, callback)]

class RequestHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		self.wfile.write('# ' + static.fqdn + ' ' + static.name + ' ' + static.version + '\n')

		while 1:
			unknown_cmd = True

			line = self.rfile.readline().rstrip()
			if not line: break

			spaced = line.split(' ')
			cmd = spaced[0]

			if len(spaced) > 1:
				args = spaced[1:]
			else:
				args = None

			if cmd == 'quit':
				break

			for item in self.server.cmds:
				if cmd == item[0]:
					unknown_cmd = False
					item[1](self, args)
					break

			if unknown_cmd:
				self.wfile.write('unknown command: ' + cmd + '\n')

	def setup(self):
		SocketServer.StreamRequestHandler.setup(self)
		host = self.client_address[0]
		port = str(self.client_address[1])
		self.server.logger.info(host + ':' + port + ' connected')

	def finish(self):
		SocketServer.StreamRequestHandler.finish(self)
		host = self.client_address[0]
		port = str(self.client_address[1])
		self.server.logger.info(host + ':' + port + ' disconnected')
