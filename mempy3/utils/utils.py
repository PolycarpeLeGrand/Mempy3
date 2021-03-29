"""General util functions"""


def yn_input(prompt='Enter y / n > '):
    """Asks for y/n input, loops until input is accepted and returns True or False"""

    r = ''
    while r not in ['y', 'n']:
        r = input(prompt).lower()
    return r == 'y'


def y_input(prompt='Enter y to continue... '):
    """Asks to enter y to continue. Returns true if y or Y, else false"""

    return input(prompt).lower() == 'y'


if __name__ == '__main__':
    print(y_input())

