import re

_RE = re.compile(
    r'(?P<start>^|[^[])\[(?P<color>\w+) (?P<text>([^\[\]]|\[\[|\]\])*)\]')
_MAP = {
    'blue': '1;34',
    'gray': '1;30',
    'green': '1;32',
    'normal': '0',
    'red': '1;31',
    'white': '0;37',
    'yellow': '1;33',
}


def shell_color(text):
    return _unescape(_RE.subn(_repl, text)[0])


def escape(text):
    return text.replace('[', '[[').replace(']', ']]')


def _repl(match):
    return '{}\033[{}m{}\033[0m'.format(
        match.group('start'), _MAP.get(match.group('color')),
        match.group('text'))


def _unescape(text):
    return text.replace('[[', '[').replace(']]', ']')