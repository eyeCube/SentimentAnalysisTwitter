import os
import sys


def decompress():
    try:
        newdir = sys.argv[1]
    except:
        print("Provide an argument for new directory name")
        sys.exit(1)

    os.system('echo Creating directory ' + newdir)
    os.system('mkdir ' + newdir)
    os.system('echo Untaring tar balls')
    os.system('tar -xf *.tar -C ' + newdir + ' --strip-components=2')
    os.system('echo Decompressing bz2 files')
    os.system('bzip2 -d ./' + newdir + '/*.bz2')
    output = os.popen('ls ./' + newdir).read()
    output = (newdir + '/ ') + output
    return output


if __name__ == "__main__":
    decompress()
