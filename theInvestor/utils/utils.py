import base64

class Utils():

    def decodeBase64(self, encodedStr: str) -> str:
        base64_bytes = encodedStr.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')

        return message

    def encodeBase64(self, decodedStr: str) -> str:
        message_bytes = decodedStr.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        return base64_message
