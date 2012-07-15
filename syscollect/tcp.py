import logging

try:
        import socketserver
except ImportError:
        import SocketServer as socketserver

import static


class ThreadedServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = 1

    def __init__(self, server_address, request_handler_class):
        tcp_server = socketserver.ThreadingTCPServer.__init__
        tcp_server(self, server_address, request_handler_class)

        self.cmds = []
        self.logger = logging.getLogger('default')

    def serve(self):
        self.serve_forever()

    def add_callback(self, cmd, callback):
        self.cmds += [(cmd, callback)]


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        banner_params = (static.fqdn, static.name, static.version)
        self.wfile.write('# %s %s %s\n' % banner_params)

        while 1:
            unknown_cmd = True

            line = self.rfile.readline().rstrip()
            if not line:
                break

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
        socketserver.StreamRequestHandler.setup(self)
        host = self.client_address[0]
        port = str(self.client_address[1])
        self.server.logger.info(host + ':' + port + ' connected')

    def finish(self):
        socketserver.StreamRequestHandler.finish(self)
        host = self.client_address[0]
        port = str(self.client_address[1])
        self.server.logger.info(host + ':' + port + ' disconnected')
