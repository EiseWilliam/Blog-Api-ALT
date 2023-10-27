from typing import Callable

VAR1: Callable[[str], str] = lambda name: 'Hello' + name + '!'



print(VAR1("John Doe"))