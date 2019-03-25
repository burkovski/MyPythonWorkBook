import time

try:
    import Crypto
    use_crypto = True
except ImportError:
    use_crypto = False


day_of_week = time.localtime(time.time())
force_readable_password = True


if not force_readable_password:
    def stringify(old):
        return old

    def unstringify(old):
        return old
else:
    separator = '-'

    def stringify(old):
        new = separator
        for code in old:
            new += str(code) + separator
        return new

    def unstringify(old):
        new = b''
        for code in old.split(separator)[1:-1]:
            new += bytes([int(code)])
        return new


if use_crypto:
    # sys.stderr.write("using PyCrypto\n")
    from Crypto.Cipher import AES
    my_key = b"pymailcgi3".ljust(16, b'=')

    def do_encode(password):
        over = len(password) % 16
        if over: password += '\0' * (16 - over)
        password = password.encode('ascii')
        aes_obj = AES.new(my_key, AES.MODE_ECB)
        return aes_obj.encrypt(password)

    def do_decode(password):
        aes_obj = AES.new(my_key, AES.MODE_ECB)
        password = aes_obj.decrypt(password)
        return password.rstrip(b'\0').decode()
else:
    # sys.stderr.write("using simple\n")
    adder = 1

    def do_encode(password):
        password = "vs{}48".format(password)
        res = ''
        for char in password:
            res += chr(ord(char) + adder)
        return res.encode()

    def do_decode(password):
        password = password[2:-2].decode()
        res = ''
        for char in password:
            res += chr(ord(char) - adder)
        return res


def encode(password):
    return stringify(do_encode(password))


def decode(password):
    return do_decode(unstringify(password))




