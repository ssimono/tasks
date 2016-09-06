import json
from itertools import chain

IN_PROGRESS = 'in-progress'
TODO = 'todo'
DONE = 'done'


def iter_status(tasks, status):
    return (task for task in tasks if task['status'] == status)


def iter_backlog(tasks):
    return chain(
        iter_status(tasks, IN_PROGRESS),
        iter_status(tasks, TODO)
    )


def iter_all(tasks):
    return chain(
        iter_backlog(tasks),
        iter_status(tasks, DONE)
    )


def find(tasks, num):
    try:
        return next(task for task in tasks if task['num'] == num)
    except StopIteration:
        return None


def next_num(tasks):
    greatest = 0

    if tasks:
        greatest = max(task['num'] for task in tasks)

    return greatest + 1


def next_backlog_num(tasks):
    try:
        return next(iter_backlog(tasks))['num']
    except StopIteration:
        return None


def load(file_name):
    try:
        return json.load(open(file_name))
    except IOError:
        return []


def dump(file_name, tasks):
    if tasks:
        json.dump(tasks, open(file_name, 'w'), sort_keys=True, indent=2)


def shell_color(color, text):
    code = {
        'blue': '1;34',
        'yellow': '1;33',
        'green': '1;32',
        'white': '0;37',
        'gray': '1;30',
    }.get(color)

    return '\033[{code}m{text}\033[0m'.format(code=code, text=text)


def render(task, mark=None, colorizer=shell_color):
    color = {
        'todo': 'blue',
        'in-progress': 'yellow',
        'done': 'green',
    }.get(task['status'], 'gray')

    if mark is None:
        symbol = ''
    elif mark:
        symbol = '*'
    else:
        symbol = ' '

    return ' '.join((
        colorizer('gray', '{symbol}#{num}'),
        colorizer(color, '{status}'),
        colorizer('white', '{title}'),
    )).format(symbol=symbol, color=color, **task)


def render_list(tasks, selected, colorizer=shell_color):
    return '\n'.join(
        render(task, task['num'] == selected, colorizer) for task in tasks
    )
