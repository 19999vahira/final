from thriftpy.rpc import make_server
from gen_py.timestamp.thrift import TimestampService
import datetime

# Implement the service handler
class TimestampHandler:
    def getTimestamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create an instance of the service handler
handler = TimestampHandler()

# Create a Thrift server
server = make_server(TimestampService, handler, '127.0.0.1', 9090)

# Start the server
print("Starting the server...")
server.serve()
print("Server stopped.")

'''# server.py
from gen_py.timestamp_service import TimestampService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from datetime import datetime
import threading

class TimestampHandler:
    def getTimestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def start_thrift_server():
    handler = TimestampHandler()
    processor = TimestampService.Processor(handler)
    transport = TSocket.TServerSocket(port=10000)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    server.serve()

# Start the Thrift server in a separate thread
thrift_server_thread = threading.Thread(target=start_thrift_server)
thrift_server_thread.daemon = True
thrift_server_thread.start()
'''