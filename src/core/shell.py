import platform
from pydoc import importfile
import subprocess
import sys
import argparse
from textwrap import wrap
import threading
from cmd import Cmd
import time
from rich.console import Console
from rich.table import Table
from rich import print
from rich.live import Live
import select
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from rich.text import Text
import colorama

from db.sortPaths import Sort
from db.utils import search_json

colorama.init()
parser = argparse.ArgumentParser(description="DrShell Command Line")
parser.add_argument(
    "-p", "--port", type=int, default=6501, help="Port for the Team Server"
)
parser.add_argument(
    "-x",
    "--signal_port",
    type=int,
    default=8080,
    help="Port for the signalShell Multi-Handler",
)
parser.add_argument(
    "-n",
    "--netcat_port",
    type=int,
    default=4443,
    help="Port for the Netcat TCP Multi-Handler",
)
parser.add_argument(
    "-f",
    "--file_smuggler_port",
    type=int,
    default=8888,
    help="Port for the HTTP File Smuggler",
)

args = parser.parse_args()

console = Console()


PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"


class MyCompleter(Completer):
    def __init__(self, cmd_instance):
        self.cmd_instance = cmd_instance

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        parts = text.split(" ")
        if len(parts) > 1 and hasattr(self.cmd_instance, "complete_" + parts[0]):
            comp_func = getattr(self.cmd_instance, "complete_" + parts[0])
            line = document.text_before_cursor
            begidx = document.cursor_position_col - len(parts[-1])
            endidx = document.cursor_position_col
            completions = comp_func(parts[-1], line, begidx, endidx)
        else:
            # استخدام الاكمال الافتراضي
            completions = self.cmd_instance.completenames(parts[0])

        for completion in completions:
            yield Completion(completion, start_position=-len(parts[-1]))


class DrShell(Cmd):
    prompt = "DrShell> "

    # intro = "Welcome to DrShell. Type help or ? to list commands."

    def __init__(self):
        super().__init__()
        self.select = []
        self.completer = MyCompleter(self)
        self.S = Sort()
        self.data = {}
        self.flag = threading.Event()
        self.sessions = {}  
        self.threads = []
        self.readjson = self.S.readJsonFile()
        self.readDirs = self.S.readDirs()
        self.session = PromptSession(
            history=InMemoryHistory(),
            # history=FileHistory('~/.myhistory'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=self.completer,
            style=Style.from_dict(
                {
                    "completion-menu.completion": "bg:#008888 #ffffff",
                    "completion-menu.completion.current": "bg:#00aaaa #000000",
                    # Prompt.
                    "username": "white",
                    "at": "white",
                    "colon": "white",
                    "pound": "white",
                    "host": "white",
                    "path": "red",
                }
            ),
            complete_in_thread=True,
        )

        # تعريف الأنماط
        style = Style(
            [
                ("username", "bold underline"),
                ("pound", "bold"),
            ]
        )
        self.prompt = [
            ("class:username", "DrShell"),
            ("class:pound", ">"),
        ]

    def get_prompt(self):
        # استخدام Text من rich مباشرة
        return Text("[bold]DrShell >[/]", style="prompt")

    def cmdloop(self, intro=None):
        self.preloop()
        if intro is not None:
            self.intro = intro
        if self.intro:
            print(self.intro)
        stop = None
        while not stop:
            try:
                line = self.session.prompt(self.prompt, complete_in_thread=True)
            except EOFError:
                line = "EOF"
            except KeyboardInterrupt:
                console.print("[red][-][white] Use 'exit -y' to leave")
                continue

            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def emptyline(self):
        pass  # Do nothing on empty input

    def default(self, line):
        if line == "":
            return  # Ignore empty input and do nothing
        else:
            console.print(f"[bold blue][*][/bold blue] exec: {line}")
            self.exec(line)

    def pprompt(self, line):
        self.prompt = line

    def exec(self, command):
        if platform.system() == "Windows":
            # تحقق من وجود الأمر
            if (
                subprocess.run(
                    f"where {command}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode
                == 0
            ):
                # تنفيذ الأمر وطباعة الإخراج
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True
                )
                print(result.stdout)
            else:
                print("Command Not Found")
        else:
            # تحقق من وجود الأمر
            if (
                subprocess.run(
                    f"command -v {command}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode
                == 0
            ):
                # تنفيذ الأمر وطباعة الإخراج
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True
                )
                print(result.stdout)
            else:
                console.print("[bold blue][*][/bold blue] Command Not Found")

    def do_search(self, args):
        search_results = search_json(json_data=self.readjson, search_word=args)
        print("\nSearch ", args.capitalize(), sep="")
        print("=" * (int(len(args)) + 5), end="\n\n")
        args = args.capitalize()

        table = Table()
        table.add_column("#")
        table.add_column("Name")
        table.add_column("Description")

        Dicts = self.readjson
        path: type[str] = str
        x = 0
        vs = []
        dicts = {}

        S = Sort()
        Dicts = self.readjson
        with Live(
            table, refresh_per_second=4
        ) as live:  # update 4 times a second to feel fluid
            x = 0
            lists = []
            for var in search_results:
                if var["keys"][0] in lists:
                    continue
                # table.add_row(str(x),var['keys'][0],var['value'])
                table.add_row(
                    str(x),
                    str(var["keys"][0])
                    .capitalize()
                    .replace(args, "[green]" + args + "[/green]")
                    .replace("./modules/", "")
                    .replace(".py", ""),
                    str(Dicts[var["keys"][0]]["description"])
                    .capitalize()
                    .replace(args, "[green]" + args + "[/green]"),
                )
                lists.append(var["keys"][0])
                x += 1
                self.select.append(str(var["keys"][0]))

    def do_use(self, args):
        try:
            int(args)
            # self.moduleIndex = 0

            file_path = self.select[int(args)]
            inps = (file_path.replace("./modules/", "")).rsplit("/")
            # console.print("[red][-][white] Invalid module index:")
            # print(file_path)
            self.module = importfile(file_path)
            inps[-1] = inps[-1].replace(".py", "")
            self.message = [
                ("class:username", "DrShell"),
                ("class:at", " "),
                ("class:host", inps[0]),
                ("class:colon", "("),
                ("class:path", "/".join(inps[1:])),
                ("class:pound", ")>"),
            ]
            self.pprompt(line=self.message)
            self.used_module = "True"
            self.select = []
        except IndexError:
            console.print("[red][-][/red] Invalid module index:")
        except:
            file_path = "./modules/" + args + ".py"
            if platform.system() == "Windows":
                inps = (args.replace("./modules/", "")).rsplit("/")
            else:
                inps = (args.replace("./modules/", "")).rsplit("/")

            self.module = importfile(file_path)
            inps[-1] = inps[-1].replace(".py", "")
            self.message = [
                ("class:username", "DrShell"),
                ("class:at", " "),
                ("class:host", inps[0]),
                ("class:colon", "("),
                ("class:path", "/".join(inps[1:])),
                ("class:pound", ")>"),
            ]
            self.pprompt(line=self.message)
            self.used_module = "True"

    def do_options(self, arg):
        if self.module is not None:
            args = arg.split()
            if not args:
                self.print_global_options()
                return

            subcommand = args[0]
            if subcommand == "-l" or subcommand == "--list":
                self.print_global_options()
            elif subcommand == "-h" or subcommand == "--help":
                self.print_global_options_help()
        else:
            print("\nNo module loaded to run.\n")
    def print_wrapped(self, title, content, indent=2, width=50):
        """طباعة نص مع التغليف والتنسيق."""

        print(f"{' ' * indent}{title}")
        wrapped_text = wrap(content, width=width)
        for line in wrapped_text:
            console.print(f"{' ' * (indent + 2)}{line}")

    def print_global_options(self):

        # طباعة المعلومات الأساسية
        basic_keys = ["name", "module", "license", "rank", "disclosed", "date"]
        for key in basic_keys:
            if key in self.module.metadata:
                print(f"    {key.capitalize()}: {self.module.metadata[key]}")

        # طباعة الأشخاص المساهمين
        if "authors" in self.module.metadata:
            print("\nProvided by:")
            for author in self.module.metadata["authors"]:
                print(f"  {author}")

        # طباعة الخيارات
        if "options" in self.module.metadata:
            print("\nBasic options:")
            print("  Name       Current Setting  Required  Description")
            print("  ----       ---------------  --------  -----------")
            for option, details in self.module.metadata["options"].items():
                setting = self.data.get(option, str(details.get("default", " ")))
                required = str(details.get("required", "no"))
                description = str(details.get("description", " "))
                wrapped_description = "\n".join(wrap(description, width=40))
                print(
                    f"  {option:<10} {setting:<15} {required:<8} {wrapped_description}"
                )

        # طباعة الوصف
        if "description" in self.module.metadata:
            self.print_wrapped("\nDescription:", self.module.metadata["description"])

        # طباعة المراجع
        if "references" in self.module.metadata:
            print("\nReferences:")
            for reference in self.module.metadata["references"]:
                print(f"  {reference['ref']}")

        # طباعة الأسماء الأخرى
        if "aka" in self.module.metadata:
            self.print_wrapped("\nAlso known as:", self.module.metadata["aka"])

        print("\nView the full module info with the info -d command.")

    def get_option_description(self, option):
        descriptions = {
            "ConsoleLogging": "Log all console input and output",
            "LogLevel": "Verbosity of logs (default 0, max 3)",
            "MeterpreterPrompt": "The meterpreter prompt string",
            "MinimumRank": "The minimum rank of exploits that will run without explicit confirmation",
            "Prompt": "The prompt string",
            "PromptChar": "The prompt character",
            "PromptTimeFormat": "Format for timestamp escapes in prompts",
            "SessionLogging": "Log all input and output for sessions",
            "SessionTlvLogging": "Log all incoming and outgoing TLV packets",
            "TimestampOutput": "Prefix all console output with a timestamp",
        }
        return descriptions.get(option, "No description available")

    def print_global_options_help(self):
        help_text = """
Usage: options [options]

Global option manipulation.

OPTIONS:
    -l, --list                List all global options
    -h, --help                Help banner
        """
        print(help_text)

    def do_run(self, args):
        if self.module is not None:
            if self.module is not None:
                if "-j" in args:
                    self.data.update({"start": 0})
                    # إنشاء خيط جديد لتشغيل الدالة run
                    thread = threading.Thread(target=self.module.run, args=(self.data,))
                    thread.start()  # بدء تشغيل الخي
                else:
                    self.data.update({"start": 1})
                    self.module.run(self.data)

                if "options" in self.module.metadata:
                    setting = {}
                    for option, details in self.module.metadata["options"].items():
                        setting.update(
                            {
                                option: self.data.get(
                                    option, str(details.get("default", " "))
                                )
                            }
                        )

                from src.core.server import check_and_start_server

                check_and_start_server(
                    str(setting["lhost"]), int(setting["lport"]), "Demo Server"
                )
        else:
            print("\nNo module loaded to run.\n")
    def complete_use(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = self.S.listmodules()  # path explotation

        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions

    def do_set(self, args=""):
        if self.module is not None:
            if args != "":
                try:
                    args = args.split(" ")
                    self.data[args[0]] = args[1]
                    print(args[0], "=>", args[1])
                except:
                    self.data[args[0]] = ""
                    print(args[0], "=>", "")
        else:
            print("\nNo module loaded.\n")
            
    def complete_set(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        dynamic_options = list(
            self.module.metadata["options"].keys()
        )  # الحصول على أسماء الخيارات من metadata

        # دمج القوائم
        options = dynamic_options

        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options

        return completions

    def do_setg(self, args):
        if self.module is not None:
            if args != "":
                try:
                    args = args.split(" ")
                    self.data[args[0]] = args[1]
                    print(args[0], "=>", args[1])
                except:
                    self.data[args[0]] = ""
                    print(args[0], "=>", "")
        else:
            print("\nNo module loaded.\n")

    def complete_setg(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ["world", "friend", "everyone"]
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions

    def do_list_payloads(self, arg):
        "List all configured payloads"
        console.print("Available payloads:")

        print("\n", "payloads".capitalize(), sep="")
        print("=" * 8, end="\n\n")
        var = self.S.listpath("./modules/" + "payloads")

        table = Table()
        table.add_column("#")
        table.add_column("Name")
        table.add_column("Description")

        S = Sort()
        Dicts = self.readjson

        with Live(
            table, refresh_per_second=4
        ) as live:  # update 4 times a second to feel fluid
            x = 0
            for i in Dicts:
                if i in var:
                    table.add_row(
                        str(x),
                        i.replace("./modules/", "").replace(".py", ""),
                        Dicts[i]["description"],
                    )
                    x += 1
                    self.select.append(str(i))

    

    def do_sessions(self, arg):
        args = arg.split()
        if "-h" in args:
            self.print_help()
        elif "-i" in args:
            index = args.index("-i") + 1
            if index < len(args):
                uid = args[index]
                self.interact_with_session(uid)
            else:
                console.print("No UID provided for interaction.", style="bold red")
        elif "-k" in args:
            index = args.index("-k") + 1
            if index < len(args):
                uid = args[index]
                self.kill_session(uid)
            else:
                console.print("No UID provided for killing session.", style="bold red")
        elif "-K" in args:
            self.kill_all_sessions()
        else:
            self.show_sessions()

    def print_help(self):
        """Print the help for the sessions command."""
        help_text = """
        Usage of the sessions command:
        -h             Show this help message
        -i <session_id>    Interact with a specified session by its ID
        -k <session_id>    Kill a specific session by its ID
        -K             Kill all sessions

        Displays active sessions if no option is provided.
        """
        console.print(help_text)

    def interact_with_session(self, uid):
        """Switch to a reverse shell session by UID."""
        if uid in self.sessions:
            session = self.sessions[uid]
            console.print(f"[bold blue][*][/bold blue] Starting interaction with [white]{uid}...[/white]")
            client_socket = session["socket"]
            from src.core.server import handle_client
            
            handle_client(uid, client_socket, session["address"])
        else:
            console.print(f"\n[bold blue][*][/bold blue] Session [{uid}] not found\n")

    def kill_session(self, uid):
        """Kill a specific session by UID."""
        console.print(f"\n[bold blue][*][/bold blue][white] Killing the following session(s): {uid}[/white]")
        if uid in self.sessions:
            session = self.sessions.pop(uid)
            console.print(f"[bold blue][*][/bold blue][white] Killing session {uid}[white]")
            session["socket"].close()
            console.print(f"[bold blue][*][/bold blue][white] {session['address']} - Command shell session {uid} closed.[white]")
            
        else:
            console.print(f"Session [{uid}] not found", style="bold red")

    def kill_all_sessions(self):
        """Kill all sessions."""
        uids = []
        for uid, session in self.sessions.items():
            uids.append(uid)
            session["socket"].close()
        console.print(f"\n[bold blue][*][/bold blue][white] Killing the following session(s): {uids}[/white]")
        self.sessions.clear()
        console.print("[bold blue][*][/bold blue] All sessions have been terminated.")

    def show_sessions(self):
        if not self.sessions:
            console.print("\nActive sessions")
            console.print("===============\n")
            console.print("No active sessions.\n")
        else:
            console.print("\nActive sessions")
            console.print("===============\n")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Session ID", style="dim", width=12)
            table.add_column("Address", min_width=20)
            table.add_column("Port", justify="right")
            table.add_column("Country", min_width=15)
            table.add_column("Device Type", min_width=20)
            for uid, info in self.sessions.items():
                table.add_row(
                    uid,
                    info['address'],
                    str(info['port']),
                    info.get('country', 'N/A'),
                    info.get('device_type', 'N/A')
                )
            console.print(table)
    def do_back(self, args):
        self.pprompt("DrShell>")
        self.module = None
        self.used_module = None

    def do_exit(self, arg):
        "Exit the server"
        
        

        for session in self.sessions.values():
            session["socket"].close()
        console.print("[bold blue][*][/bold blue] Exiting the DrShell...")
        
        # إشارة للخيوط للتوقف
        self.flag.set()
        time.sleep(3)
        sys.exit()
