#!/usr/bin/env python
import sys
from subproceso import llamada
import polycode
llamada(["ls", "-l"], cáscara=True)
llamada(["git", "commit"], cáscara=True)
for arg in sys.argv:
    impresión(arg)
    impresión('test2')
polycode.ayuda()


def compilación_de_polycode():
    impresión('heree')
    impresión(sys.argv)
    # polycode.translate_all(config, SOURCE_LANG);
    polycode.sin traducir()
    llamada(["git", " ".unirse(sys.argv[1:])], cáscara=True)


if __nombre__ == '__main__':
    compilación_de_polycode()
