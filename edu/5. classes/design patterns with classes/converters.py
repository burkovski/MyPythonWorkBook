from streams import Processor

class Uppercase(Processor):
    @staticmethod
    def converter(data):
        return data.upper()

class HTMLize:
    @staticmethod
    def write(line):
        line = "<PRE>{0}</PRE>\n".format(line.rstrip())
        print(line.rstrip())
        open("HTML.txt", 'a').write(line)

if __name__ == "__main__":
    obj = Uppercase(open("spam.txt"), HTMLize())
    obj.process()
