import socketserver
import datetime

def log(message):
    print("{}: {}".format(datetime.datetime.now(datetime.timezone.utc), message))

class ServerHandler(socketserver.StreamRequestHandler):
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        log("{} wrote:".format(self.client_address[0]))
        print(self.data)

        if str(self.data, "utf-8") == "close":
            self.shutdown()
            print("connection closed")
            return

        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

    def handle_error(request, client_address):
        log("shuting down connection to {}".format(client_address))
