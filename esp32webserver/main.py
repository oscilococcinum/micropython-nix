import esp
from machine import Pin
import network
try:
    import usocket as socket
    print('Imported usocket')
except:
    import socket
    print('Imported socket')
import gc
esp.osdebug(None) #type: ignore
gc.collect()


class Esp32:
    def __init__(self) -> None:
        self.wlan = network.WLAN(network.STA_IF)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.led = Pin(2, Pin.OUT)


        self.wlan.active(True)
        self.wlan.connect('PLAYA15ECD4', 'Yfzs3xfphhsa')
        while self.wlan.isconnected() == False:
            pass
        print('Connection successful')
        print(self.wlan.ifconfig())

        self.socket.bind(('', 80))
        self.socket.listen(5)

    def getWebPageHtml(self, gpioState: str):
        return '''
        <html>
        <head>
            <title>ESP Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style>
                html {
                    font-family: Helvetica;
                    display: inline-block;
                    margin: 0px auto;
                    text-align: center;
                }

                h1 {
                    color: #0F3376;
                    padding: 2vh;
                }

                p {
                    font-size: 1.5rem;
                }

                .button {
                    display: inline-block;
                    background-color: #e7bd3b;
                    border: none;
                    border-radius: 4px;
                    color: white;
                    padding: 16px 40px;
                    text-decoration: none;
                    font-size: 30px;
                    margin: 2px;
                    cursor: pointer;
                }

                .button2 {
                    background-color: #4286f4;
                }
            </style>
        </head>
        <body>
            <h1>ESP Web Server</h1>
            <p>GPIO state: <strong>''' + gpioState + '''</strong></p>
            <p><a href="/?led=on"><button class="button">ON</button></a></p>
            <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
        </body>
        </html>'''


esp32 = Esp32()
while True:
    conn, addr = esp32.socket.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024).decode()
    print('Content = %s' % request)
    if request.find('/?led=on') == 4:
        print('LED ON')
        esp32.led.value(1)
    elif request.find('/?led=off') == 4:
        print('LED OFF')
        esp32.led.value(0)
    else:
        print('Pass')
        pass
    response = esp32.getWebPageHtml(str(esp32.led.value()))
    conn.send(b'HTTP/1.1 200 OK\n')
    conn.send(b'Content-Type: text/html\n')
    conn.send(b'Connection: close\n\n')
    conn.sendall(response.encode('utf-8'))
    conn.close()
