'''
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift_final.gen_py.timestamp import TimestampService

def get_timestamp():
    transport = TSocket.TSocket('localhost', 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = TimestampService.Client(protocol)

    try:
        transport.open()
        timestamp = client.getTimestamp()
        return timestamp
    finally:
        transport.close()

print("Timestamp from server:", get_timestamp())'''

