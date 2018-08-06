#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

cmd = 'ls'
arg1 = ' -shlat'
os.system(cmd + arg1)

url_dict = {}

with open('pi_digits.text') as file_object:
        contents = file_object.read()
        print(type(contents))
        print(contents)
#        for url in contents:
            
config = {}
with open('env_db.conf') as file:
           for line in file.readlines():
               try:
                   config[line.split('=')[0].strip(' ')] = line.split('=')[1].strip(' ').strip('\n')
               except:
                   print('Config format is incurrent!')
                   raise Exception('Config format is incurrent!')
        return config







