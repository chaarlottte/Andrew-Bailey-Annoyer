import base64

class b64utils():
    def b64_to_wav(base64_string: str, output_file_path: str) -> None:
        decode_string = base64.b64decode(base64_string)
        with open(output_file_path, "wb") as f:
            f.write(decode_string)
            f.close()

