import os
import sys
import re
import getopt

scriptBaseDir = '/root/projects/DataForPreprocess/Scripts/'


def main(argv):
    autoRunScriptDir = ''
    subjectDir = ''
    try:
        opts, args = getopt.getopt(argv, "hD:", ["help", "subjectDir="])
    except getopt.GetoptError:
        print('2.auto1.py -h -D <subjectDir>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('2.auto1.py -S <autoRunScriptDir> -D <subjectDir>')
            sys.exit()
        elif opt in ("-D", "--subjectDir"):
            subjectDir = arg

    if subjectDir != '':
        os.chdir(subjectDir + '1.ciftify/ciftify_data')
        files = os.listdir(os.getcwd())
        for file in files:
            pattern = re.compile(r'^sub-')
            match = pattern.match(file)
            if match:
                arg = file.split('-')[1]
                subid = arg[0:5] + '_' + arg[5:8] + '_S_' + arg[9:]
                # for example : subid = 'ADNI2_002_S_1234'
                command = ''.join(
                    ('python ',
                     scriptBaseDir,
                     '1.ciftify.py ',
                     subid,
                     ' ',
                     subjectDir + '1.ciftify/'))
                os.system(command)
                print(command)


# Usage:
# python  2.auto1.py  -D subjectDir
# Example cmd:
# python  /root/projects/DataForPreprocess/Scripts/2.auto1.py -D /root/projects/DataForPreprocess/Data/664908ce-a6ab-42b2-9c0a-0228035e980b
if __name__ == "__main__":
    main(sys.argv[1:])
