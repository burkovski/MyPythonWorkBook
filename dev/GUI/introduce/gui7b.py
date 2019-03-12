from gui7 import HelloPackage


class ExtendHelloPackage(HelloPackage):
    def __getattr__(self, item):
        return getattr(self.top, item)      # передать вызов настоящему виджету


if __name__ == '__main__':
    ExtendHelloPackage().mainloop()
