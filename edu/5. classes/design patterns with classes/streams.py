class Processor:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
    def process(self):
        for line in self.reader:
            line = self.converter(line)
            self.writer.write(line)
    def converter(self, data):
        raise Exception("Converter must be defined")    # Возбудить исключение
