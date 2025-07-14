import chardet

class EncodingDetector:
    def __init__(self, file):
        self.file = file
        self.encoding = None

    def detect(self):
        result = chardet.detect(self.file.read())
        self.file.seek(0)  # Reset file pointer after reading
        self.encoding = result['encoding']
        return self.encoding