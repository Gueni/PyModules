#!/usr/bin/env python
# coding=utf-8

import pyfiglet
import sys

def figlet_comment_block(text: str, font: str = 'slant'):
    fig = pyfiglet.Figlet(font=font)
    rendered = fig.renderText(text)
    for line in rendered.splitlines():
        print(f"#?             {line}")

if __name__ == "__main__":

        word = "PYMOS"
        figlet_comment_block(word)
