import threading
import time
from src.core.server import app 
from src.core.server import start_server 
import argparse
import threading
import time
from rich.console import Console
from rich import print
import colorama


colorama.init()
parser = argparse.ArgumentParser(description="DrShell Command Line")
parser.add_argument("-p", "--port", type=int, default=6501, help="Port for the Team Server")
parser.add_argument("-x", "--signal_port", type=int, default=8080, help="Port for the signalShell Multi-Handler")
parser.add_argument("-n", "--netcat_port", type=int, default=4443, help="Port for the Netcat TCP Multi-Handler")
parser.add_argument("-f", "--file_smuggler_port", type=int, default=8888, help="Port for the HTTP File Smuggler")

args = parser.parse_args()

console =  Console()




def main():
    
    # تعريف النص مع الروابط والتدرج اللوني
    console.print(r"""
    ________            _________      .__  .__   
    \______ \_______   /   _____/ ____ |  | |  |  
    |    |  \_  __ \  \_____  \_/ __ \|  | |  |  
    |    `   \  | \/  /        \  ___/|  |_|  |__
    /_______  /__|    /_______  /\___  >____/____/
            \/                \/     \/   
                                                
            
                    By [link=https://github.com/DrDataYE]@DrDataYE[/link]
                    
    \[[bold green]Info[/bold green]] Follow on [link=https://x.com/DrDataYE]Twitter[/link], [link=https://github.com/DrDataYE]GitHub[/link], [link=https://t.me/DrDataYE]Telegram[/link], [link=https://youtube.com/DrDataYE]Youtube[/link]
    \[[bold green]Info[/bold green]] Thank you!              
    """) 
    threading.Thread(target=start_server, args=("0.0.0.0", args.port, "Team Server")).start()
    threading.Thread(target=start_server, args=("0.0.0.0", args.signal_port, "signalShell Multi-Handler")).start()
    threading.Thread(target=start_server, args=("0.0.0.0", args.netcat_port, "Netcat TCP Multi-Handler")).start()
    threading.Thread(target=start_server, args=("0.0.0.0", args.file_smuggler_port, "HTTP File Smuggler")).start()
    time.sleep(1)
    console.print("\nWelcome to DrShell. Type help or ? to list commands.\n",style="bold")

    while True:
            try:
                app.cmdloop()
            except KeyboardInterrupt:
                print("Use 'exit -y' to leave")
                
