import base64
from urllib.parse import quote


class ShellcodeEncoder:
    def __init__(self, shellcode):
        if isinstance(shellcode, str):
            self.shellcode = shellcode.encode()  # تحويل النص إلى bytes إذا كان نصاً
        else:
            self.shellcode = shellcode

    def url_encode(self):
        return quote(self.shellcode)

    def double_url_encode(self):
        # تنفيذ URL encode مرتين
        return quote(quote(self.shellcode))

    def base64_encode(self):
        return base64.b64encode(self.shellcode).decode("utf-8")

    def base32_encode(self):
        return base64.b32encode(self.shellcode).decode("utf-8")
