from multiprocessing import Process, Queue
from queue import Empty
import socket
import os
import sys
from time import time
from io import TextIOWrapper
from settings import UDP_IP, UDP_PORT
import json

class ACounter:
  def __init__(self, count_type: str='10s') -> None:
    self.count_type = count_type
    self.a1_sum = 0
    self.a2_max = 0
    self.a3_min = -1
  
  def clear(self) -> None:
    self.a1_sum = 0
    self.a2_max = 0
    self.a3_min = -1

  def update(self, data: dict) -> None:
    a1 = data['A1']
    a2 = data['A2']
    a3 = data['A3']
    self.a1_sum += a1
    self.a2_max = max(a2, self.a2_max) 
    if self.a3_min == -1:
      self.a3_min = a3
    else:
      self.a3_min = min(a3, self.a3_min)
  
  def get(self, timestamp: int) -> dict:
    return {
      'timestamp': timestamp,
      'count_type': self.count_type,
      'A1_sum': self.a1_sum,
      'A2_max': self.a2_max,
      'A3_min': self.a3_min if self.a3_min != -1 else 0
    }
  
  def get_and_clear(self, timestamp: int) -> dict:
    out = self.get(timestamp)
    self.clear()
    return out


def reciever(q: Queue) -> None:
  sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((UDP_IP, port))
  print(f"Started UDP reciever {os.getpid()}")
  while True:
    try:
      data = sock.recv(1024)
    except IOError:
      sock.close()
      break
    except KeyboardInterrupt:
      sock.close()
      break
    # print(f"Received message on {os.getpid()}: {data}")
    try:
      decoded = json.loads(data.decode())
    except:
      continue
    q.put(decoded)
            
def main_loop(q: Queue, out_file: TextIOWrapper) -> None:
    last_time = time() # Время последней записи
    elapsed_blocks = 0 # Количество прошедших 10-секундных блоков
    aCounter, aCounter60 = ACounter('10s'), ACounter('60s')
    while True:
      current_time = time()
      left_time = 10 - (current_time - last_time)

      if left_time < 0:
        elapsed_blocks += 1
        out_data = aCounter.get_and_clear(int(current_time))
        print(out_data)
        print(out_data, file=out_file)
        if elapsed_blocks == 6:
          elapsed_blocks = 0
          out_data = aCounter60.get_and_clear(int(current_time))
          print(out_data)
          print(out_data, file=out_file, flush=True)
        last_time += 10
        continue

      try:
        data = q.get(block=True, timeout=left_time)
      except Empty:
        continue
      aCounter.update(data)
      aCounter60.update(data)

def main(port: int) -> None:
    q = Queue() # Queue for values
    cpu_count = os.cpu_count()
    # cpu_count = 4
    recievers = [ Process(target=reciever, args=(q, )) for _ in range(cpu_count) ]
    out_file = open('out.log', 'a')
    for r in recievers: r.start()
    try:
      main_loop(q, out_file)
    except KeyboardInterrupt:
      pass
    print('\nClosing socket and output file...')
    for r in recievers: r.join()
    out_file.close()
    print('Exiting program.')




if __name__ == '__main__':
  print(f"Program started {os.getpid()}")
  if len(sys.argv) > 1:
    port = sys.argv[1]
  else:
    port = UDP_PORT
  main(port=UDP_PORT)