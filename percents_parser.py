import re


class FakeTokenException(BaseException):
    pass


def parse_line(any_str, line_num, sep_tokens, perc_pattern):
    tokens = any_str.split(sep_tokens)
    for ix, token in enumerate(tokens):
        try:
            if not perc_pattern.match(token):
                raise ValueError
        except ValueError:
            raise FakeTokenException(
                "<Error in line #{}: '{}'; token #{}: '{}'>".format(
                    line_num, any_str, ix+1, tokens[ix]))


def parse_file(path, *, sep_tokens):
    perc_pattern = re.compile(r"^\d+%$")
    with open(path) as file:
        for ix, line in enumerate(file, start=1):
            try:
                parse_line(line, ix, sep_tokens, perc_pattern)
            except FakeTokenException as exc:
                print(exc)
                break
        else:
            print("No errors in file!")


if __name__ == "__main__":
    parse_file(r"C:\Users\HP\Documents\percents.txt", sep_tokens='; ')
