import asyncio
import socket
import ssdp
import aiohttp
import aiohttp_jinja2
import jinja2
import pathlib

from protocol import SSDPProtocol
from routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent
SSDP_PORT = 1900
SSDP_HOST = '239.255.255.250'

def get_discover_message():
    message = ('M-SEARCH * HTTP/1.1\r\n' +
                'HOST: {}:{}\r\n' +
                'MAN: "ssdp:discover"\r\n' +
                'MX: 1\r\n' +
                'ST: ssdp:all\r\n' +
                '\r\n')
    
    return message.format(SSDP_HOST,SSDP_PORT)

def server_loop():
    
    loop = asyncio.get_event_loop()
    connect = loop.create_datagram_endpoint(SSDPProtocol, family=socket.AF_INET)
    transport, protocol = loop.run_until_complete(connect)
    notify = ssdp.SSDPRequest(get_discover_message())
    notify.sendto(transport, (SSDPProtocol.MULTICAST_ADDRESS, 1900))
    app = aiohttp.web.Application()
    app['protocol'] = protocol
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / 'upnp-rest-server' / 'templates')))
    #Start server in http://0.0.0.0:8080/
    runner = aiohttp.web.AppRunner(app)
    setup_routes(app)
    loop.run_until_complete(runner.setup())
    site = aiohttp.web.TCPSite(runner)    
    loop.run_until_complete(site.start())

    try:
        loop.run_forever()
        print("Exit")
    except KeyboardInterrupt:
        pass
    transport.close()
    loop.close()

def main():
    server_loop()
    
if __name__ == '__main__':
    main()