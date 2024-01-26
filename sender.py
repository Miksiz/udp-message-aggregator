import socket
import os
from settings import UDP_IP, UDP_PORT
from time import sleep

print(f"Started sender {os.getpid()}")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
to_send = [
    b'{"A1":1, "A2":10, "A3":100}',
    0.5,
    b'{"A1":2, "A2":12, "A3":102}',
    b'{"A1":3, "A2":30, "A3":130}',
    2,
    b'{"A1":4, "A2":20, "A3":200}',
    b'{"A1":5, "A2":13, "A3":103}',
    b'{"A1":6, "A2":40, "A3":140}'
]
pause = True
for data in to_send:
    if isinstance(data, (int, float)):
        sleep(data)
        continue
    if pause: sleep(0.1)
    print(f"Sent {data} from sender")
    sock.sendto(data, (UDP_IP, UDP_PORT))
sock.close()

# echo -n "hello" | nc -u -w 1 127.0.0.1 8000
# for i in `seq 10`; do echo -n "hello $i" | nc -u -w 1 127.0.0.1 8000; done