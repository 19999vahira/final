from gen_py.timestamp.thrift import TimestampService
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def get_timestamp():
    # Create a socket to connect to the Thrift server
    transport = TSocket.TSocket('localhost', 10000)

    # Buffer the transport
    transport = TTransport.TBufferedTransport(transport)

    # Use binary protocol to serialize/deserialize data
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = TimestampService.Client(protocol)

    try:
        # Open the transport
        transport.open()

        # Call the service to get the current timestamp
        timestamp = client.getTimestamp()

        return timestamp

    finally:

        transport.close()

# Call get_timestamp() whenever you need a timestamp

'''from gen_py.timestamp_service import TimestampService
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    # Make socket
    transport = TSocket.TSocket('localhost', 10000)
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = TimestampService.Client(protocol)

    # Connect!
    transport.open()

    # Call the service
    print("Timestamp from server:", client.getTimestamp())

    # Close!
    transport.close()

except Thrift.TException as tx:
    print('%s' % tx.message)
'''
