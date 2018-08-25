#!/usr/bin/env python
import sys
from subprocess import call
import polycode
call(["ls", "-l"], shell=True)
call(["git", "commit"], shell=True)
for arg in sys.argv:
    print(arg)
    print('test2')
polycode.help()


def polycode_commit():
    print('heree')
    print(sys.argv)
    # polycode.translate_all(config, SOURCE_LANG);
    polycode.untranslate()
    call(["git", " ".join(sys.argv[1:])], shell=True)


if __name__ == '__main__':
    polycode_commit()
