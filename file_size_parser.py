import re


class FakeTokenException(BaseException):
    pass


def parse_line(any_str, line_num, sep_tokens, sep_in_token, num_pattern, val_pattern):
    tokens = any_str.split(sep_tokens)
    split_tokens = [token.split(sep_in_token) for token in tokens]
    for ix, token in enumerate(split_tokens):
        try:
            num, val = token
            if not num_pattern.match(num):
                raise ValueError
            if not val_pattern.match(val):
                raise ValueError
        except ValueError:
            raise FakeTokenException(
                "<Error in line #{}: '{}'; token #{}: '{}'>".format(
                    line_num, any_str, ix+1, tokens[ix]))


def parse_file(path, *, sep_tokens, sep_in_token):
    num_pattern = re.compile(r"\d+")
    val_patter = re.compile(r"(?:^Kilo|^Mega|^Giga|^Tera)?bytes{1}$|^[KMGT]?b{1}$")
    with open(path) as file:
        for ix, line in enumerate(file, start=1):
            try:
                parse_line(line, ix, sep_tokens, sep_in_token, num_pattern, val_patter)
            except FakeTokenException as exc:
                print(exc)
                break
        else:
            print("No errors in file!")


if __name__ == "__main__":
    parse_file(r"C:\Users\HP\Documents\files_info.txt", sep_tokens='; ', sep_in_token=' ')
