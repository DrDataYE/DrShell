import datetime
import select
import socket
import sys
import threading
from rich.console import Console

from src.core.shell import DrShell

app = DrShell()

console = Console()
from datetime import datetime
import pytz

def get_current_time(timezone_str='Asia/Riyadh'):
    # تعيين المنطقة الزمنية
    timezone = pytz.timezone(timezone_str)
    # الحصول على الوقت الحالي مع المنطقة الزمنية
    now = datetime.now(timezone)
    # تنسيق الوقت للصيغة المطلوبة
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S %z')
    return formatted_time



import socket
import struct

def get_os_from_socket(client_socket):
    try:
        client_socket.settimeout(3)  # تحديد وقت محدود للانتظار
        raw_data, _ = client_socket.recvfrom(65535)
        if len(raw_data) < 20:
            # لا يوجد بيانات كافية لتحليل رأس الحزمة
            return "Unknown"

        ip_header = raw_data[0:20]
        ip_hdr = struct.unpack('!BBHHHBBH4s4s', ip_header)
        ttl = ip_hdr[5]
        
        if ttl <= 64:
            return "Linux/Unix or Mac OS"
        elif ttl <= 128:
            return "Windows"
        else:
            return "Unknown"
    except socket.timeout:
        # يحدث هذا الاستثناء إذا لم تتلقَ أية بيانات في الفترة الزمنية المحددة
        return "Unknown"
    except Exception as e:
        return "Unknown"






# def start_server(host, port, description):

#     try:
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((host, port))
#         server_socket.listen(5)
#         console.print(
#             f"[bold blue][+] [white not bold]Start Lisning in {host}:{port} on {description}."
#         )
        
#         sessions = 0
#         while not app.flag.is_set():
#             client_socket, addr = server_socket.accept()
#             # استخدم دالة get_os_from_socket لتحديد نوع نظام التشغيل
#             os_type = get_os_from_socket(client_socket)
#             sessions += 1
#             uid = str(sessions)
#             app.sessions[uid] = {
#                 "socket": client_socket,
#                 "address": addr[0],
#                 "port": addr[1],
#                 "device_type": os_type
#             }
#             console.print(f"\n[bold blue][*][/bold blue] Command shell session {uid} opened ({host}:{port} -> {addr[0]}:{addr[1]}) at {get_current_time()}", style="bold")
#     except:
#         console.print(
#             f"[bold blue][*][/bold blue] [white]{host}:{port} is already listening.[/white]"
#         )

# def start_server(host, port, description):
#     try:
#         server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_socket.bind((host, port))
#         server_socket.listen(5)
#         console.print(
#             f"[bold blue][+] [white not bold]Start Listening in {host}:{port} on {description}."
#         )

#         while not app.flag.is_set():
#             client_socket, addr = server_socket.accept()
#             if app.flag.is_set():
#                 client_socket.close()
#                 break
#             # Process client_socket as usual
#             os_type = get_os_from_socket(client_socket)
#             uid = str(len(app['sessions']) + 1)
#             app['sessions'][uid] = {
#                 "socket": client_socket,
#                 "address": addr[0],
#                 "port": addr[1],
#                 "device_type": os_type
#             }
#             console.print(f"\n[bold blue][*][/bold blue] Command shell session {uid} opened ({host}:{port} -> {addr[0]}:{addr[1]}) at {get_current_time()}", style="bold")
    
#     except Exception as e:
#         console.print(
#             f"[bold blue][*][/bold blue] Error: {e}"
#         )
#     finally:
#         server_socket.close()
#         console.print(
#             f"[bold blue][*][/bold blue] Server on {host}:{port} has been shut down."
#         )

import socket
import threading
import select
from rich.console import Console

console = Console()




def start_server(host, port, description):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.setblocking(0)  # Make the socket non-blocking
    console.print(f"[bold blue][+] [white not bold]Start Listening in {host}:{port} on {description}.")

    try:
        while not app.flag.is_set():
            # Check for new connections, but don't block
            ready_to_read, _, _ = select.select([server_socket], [], [], 0.5)
            if ready_to_read:
                client_socket, addr = server_socket.accept()
                uid = str(len(app.sessions) + 1)
                app.sessions[uid] = {
                    "socket": client_socket,
                    "address": addr[0],
                    "port": addr[1],
                    "device_type": "Unknown"  # Assuming get_os_from_socket is defined elsewhere
                }
                console.print(f"\n[bold blue][*][/bold blue] Command shell session {uid} opened ({host}:{port} -> {addr[0]}:{addr[1]}) at {get_current_time()}")

    except Exception as e:
        console.print(f"[bold red][*][/bold red] Error: {e}")
    finally:
        server_socket.close()
        console.print(f"[bold blue][*][/bold blue] Server on {host}:{port} has been shut down.")
        for session in app.sessions.values():
            session['socket'].close()
        for t in app.threads:
            t.join()



def check_and_start_server(lhost, lport, description):
    thread = threading.Thread(target=start_server, args=(lhost, lport, description))
    thread.start()
    app.threads.append(thread)




def handle_client(uid, client_socket, client_address):
    console.print(f"[bold blue][*][/bold blue] You can use the [green]exit[/green] or [green]background[/green] command to exit the session.")

    try:
        buffer = []
        while True:
            # Wait for input from the user or the client
            ready_to_read, _, _ = select.select([client_socket, sys.stdin], [], [])

            for source in ready_to_read:
                if source == client_socket:
                    while True:
                        data = client_socket.recv(4096)
                        if not data:
                            if buffer:
                                full_data = ''.join(buffer)
                                sys.stdout.write(full_data)
                                sys.stdout.flush()
                                buffer = []  # Clear buffer
                            session = app.sessions.pop(uid)
                            session["socket"].close()
                            console.print(f"[bold blue][*][/bold blue] {client_address} - Command shell session {uid} closed.  Reason: User exit")
                            return
                        buffer.append(data.decode("utf-8"))
                        if len(data) < 4096:
                            # If less than 4096 bytes, likely the end of the message
                            full_data = ''.join(buffer)
                            sys.stdout.write(full_data)
                            sys.stdout.flush()
                            buffer = []  # Clear buffer after processing
                            break
                else:
                    # Get input from the server user and send it to the client
                    cmd = sys.stdin.readline()
                    if cmd.strip().lower() in {"exit", "background"}:
                        ask = input(f"{cmd.strip().lower().capitalize()} session ? [y/N]")
                        if ask.lower() == "y":
                            
                            action = "Exiting" if cmd.strip().lower() == "exit" else "Backgrounding"
                            console.print(f"\n[bold blue][*][/bold blue] {action} session.")
                            if cmd.strip().lower() == "exit":
                                console.print(f"[bold blue][*][/bold blue] Connection closed with {client_address}")
                                client_socket.close()
                            return  # Exit the loop but do not close the socket
                    client_socket.send(cmd.encode("utf-8"))

    except Exception as e:
        console.print(f"[bold red][-][/bold red]Error with {client_address}: {e}")
        client_socket.close()

