import itertools
import subprocess
import sys
from random import randint as r
from os import system as s

chars = ('1234567890')

n = int(input('Введите кол-во символов в пароле: '))
password = ''

for i in range(n):
    password = f'{password}{chars[r(0, len(chars)-1)]}'
    for password in itertools.product(chars, repeat=n):
        password = "".join(password)

        file = open('output8.txt', 'w')
        file.write(allpasswords)