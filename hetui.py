#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from subprocess import Popen, PIPE

class HeTUIApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F  = npyscreen.Form(name = "Welcome to He Tui (Helang TUI)",)

        fn = F.add(npyscreen.TitleFilename, name = "何代码:", value="great.he")
        t2 = F.add(npyscreen.BoxTitle, name="垃圾桶:", editable=False)
        
        t2.entry_widget.scroll_exit = True
        t2.values = []

        while True:
            # This lets the user interact with the Form.
            F.edit()
            try:
                t2.values = []
                with open(fn.value, "r") as f:
                    cmd = ["python", "-c", f"""
from helang.lexer import Lexer
from helang.parser import Parser

with open('{fn.value}', 'r') as f:
    content = f.read()
    lexer = Lexer(content)
    parser = Parser(lexer.lex())
    env = dict()
    parser.parse().evaluate(env)
                    """]
                    process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    output, errors = process.communicate()
                    t2.values = output.decode().split("\n")
            except Exception as e:
                t2.values = [f"执行'{fn.value}'代码文件失败"]

if __name__ == "__main__":
    App = HeTUIApp()
    App.run()
