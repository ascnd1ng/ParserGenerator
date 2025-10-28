import re


def lexer(text, patterns):
    tokens = []
    position = 0
    line = 1
    column = 1

    while position < len(text):
        matched = False
        best_match = None
        best_length = 0
        best_tag = None

        for pattern, tag in patterns:
            regex = re.compile(pattern)
            match = regex.match(text, position)
            if match:
                value = match.group(0)
                length = len(value)
                if length > best_length:
                    best_match = match
                    best_length = length
                    best_tag = tag

        if best_match:
            value = best_match.group(0)
            tokens.append([best_tag, (line, column), value])
            position = best_match.end()
            column += len(value)
            matched = True

        if not matched:
            if text[position] in [' ', '\n', '\t']:
                if text[position] == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                position += 1
            else:
                print(f"Syntax error ({line}, {column}): Unexpected character '{text[position]}'")
                position += 1
                column += 1
    tokens.append(['$'])
    return tokens