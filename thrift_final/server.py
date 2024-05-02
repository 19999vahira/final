'''from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from gen_py.timestamp import TimestampService
import datetime

class TimestampHandler:
    def getTimestamp(self):
        uk_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1)))
        return uk_time.strftime("%Y-%m-%d %H:%M:%S")

handler = TimestampHandler()
processor = TimestampService.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting the server...")
server.serve()
print("Server stopped.")'''


