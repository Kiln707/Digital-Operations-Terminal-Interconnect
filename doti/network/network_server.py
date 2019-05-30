from tornado.tcpserver import TCPServer as _TCPServer
from tornado.tcpserver import TCPClient as _TCPClient
import socket

class TCPServer(_TCPServer):
    def __init__(self, callback, ssl_options: Union[Dict[str, Any], ssl.SSLContext] = None, max_buffer_size: int = None, read_chunk_size: int = None):
        super().__init__(self, ssl_options=ssl_options, max_buffer_size=max_buffer_size, read_chunk_size=read_chunk_size)
        self.handle=handle

    async def handle_stream(self, stream, address):
        await self.handle(stream=stream, address=address)

class TCPClient(_TCPClient):
    def __init__(self, host, port, family=socket.AF.UNSPEC, ssl_options=None, max_buffer_size=None, source_ip=None, source_port=None, timeout=None, resolver=None):
        super().__init__(resolver=resolver)
        self._stream=self.connect(host=host, port=port, af=family, ssl_options=ssl_options)
