from rich.console import Console
from rich.table import Table
from curtsies import Input

console = Console()
keyUp = 'KEY_UP'
keyDown = 'KEY_DOWN'
keyLeft = 'KEY_LEFT'
keyRight = 'KEY_RIGHT'

def clearStyleTags(inputs):
    result = []
    for i in inputs:
        i = i.replace('[red]', '')
        i = i.replace('[/]', '')
        result.append(i)
    return result

def getUserInput(header, options):
    x, y = 0, 0
    hasResult = False
    maxY = len(options)
    maxX = len(options[0])

    while True:
        console.clear()
        table = Table(show_header=True, header_style="bold magenta")
        for head in header:
            table.add_column(head)

        i = 0
        for option in options:
            if len(header) != len(options[0]):
                continue
            option = clearStyleTags(option)
            if y == i:
                option[x] = "[red]" + option[x] + "[/]"
            table.add_row(*option)

            i = i + 1
        console.print(table)

        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                if e == keyUp:
                    y = y - 1
                    if y < 0:
                        y = maxY - 1
                    break
                elif e == keyDown:
                    y = y + 1
                    if y >= maxY:
                        y = 0
                    break
                elif e == keyLeft:
                    x = x - 1
                    if x < 0:
                        x = maxX - 1
                    break
                elif e == keyRight:
                    x = x + 1
                    if x >= maxX:
                        x = 0
                    break
                elif e == '\n':
                    return options[y][x]


console.clear()
while True:
    userInput = getUserInput(['Test1', 'Test2'], [["abc1", "abc2"], ['abc3', 'abc4']])
    console.print(userInput)
