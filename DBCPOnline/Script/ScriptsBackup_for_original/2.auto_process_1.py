import os
import sys
import re

if __name__ == "__main__":
    if len(sys.argv) == 2:
        rootDir = os.chdir(os.path.split(sys.argv[1])[0])
        files  = os.listdir(os.getcwd())
        for file in files:
            pattern = re.compile(r'^sub-')
            match = pattern.match(file)
            if match:
                arg = file.split('-')[1]
                subid = arg[0:5] + '_' + arg[5:8] + '_S_' + arg[9:]
                command = 'python /root/PycharmProjects/ciftify/1.ciftify.py ' + subid
                os.system(command)
