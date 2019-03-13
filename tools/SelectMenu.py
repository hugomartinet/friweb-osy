import sys

from getch import getch

from tools.Color import Color


class SelectMenu:

    def __init__(self, title, choices):
        self.title = title
        self.choices = choices
        self.cursor = 0


    def listen_to_keyboard(self):
        cmd = ''
        while cmd not in ['\033', '\n']:
            cmd = getch()

        if cmd == '\n':
            return 'ENTER'

        getch()
        key = getch()
        return 'UP' if key == 'A' else ('DOWN' if key == 'B' else self.listen_to_keyboard())


    def print_menu(self):
        print(Color.BOLD + self.title + Color.END)

        for choice in self.choices:
            if self.choices.index(choice) == self.cursor:
                print(Color.CYAN + '> ' + choice + Color.END)
            else:
                print('  ' + choice)


    def run(self):
        cmd = ''
        self.print_menu()

        while cmd != 'ENTER':
            if cmd == 'UP':
                self.cursor = (self.cursor - 1) % len(self.choices)
            elif cmd == 'DOWN':
                self.cursor = (self.cursor + 1) % len(self.choices)

            sys.stdout.write('\033[F' * (len(self.choices) + 1))
            self.print_menu()
            cmd = self.listen_to_keyboard()

        print('\n')
        return self.cursor