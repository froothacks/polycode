import os
import sys
import json
from fnmatch import fnmatch
import peticiones
# from lib import lib as lib_inst

# Polyglot

TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO = '.polycode'
TRADUCIR_IGNORAR_NOMBRE_DE_ARCHIVO = '.polycodeignore'
TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL = '.polycodetmp'

PLANTILLA_DE_RUTA_DE_ARCHIVOS_TRADUCIDOS = 'repo-{}/'
TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT = '.polycodedata/'
URL_DEL_SERVIDOR = 'https://davidgu.stdlib.com/polycode@dev'


def ayuda():
    texto de ayuda = """
    Usage: polycode [--help] [Destination Language]

    Examples:
      polycode untranslate
      polycode translate ES -> Translates current project into Spanish
      polycode --f targetfile ES -> Translates file 'targetfile' into Spanish
    """
    impresión(texto de ayuda)


def traducir_archivo(config, archivo_de_destino, FUENTE_LANG, DEST_LANG):
    """
    Translate a specific file
    """

    with abierto(archivo_de_destino) as f:
        fuente = f.leer()

    ruta_del_archivo_de_mapa = TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT + '{}.map'.formato(archivo_de_destino)
    mapa = {}
    if os.camino.isfile(ruta_del_archivo_de_mapa):
        with abierto(ruta_del_archivo_de_mapa) as f:
            mapa = f.leer()
            mapa = json.cargas(mapa)

    # result = lib_inst.davidgu.polycode['@dev'](source, config, map)
    carga útil = {'doc': fuente, 'from': FUENTE_LANG, 'to': DEST_LANG, 'map': mapa}
    req = peticiones.obtener(URL_DEL_SERVIDOR, params=carga útil)
    resultado = json.cargas(req.texto)

    traducido = resultado['doc']
    mapa_de_traducción = json.deshecho(resultado['map'])

    # Translations overwrite the translated file
    ruta_de_archivo_traducida = archivo_de_destino
    ruta_del_mapa_de_traducción = ruta_del_archivo_de_mapa

    # Write received files
    with abierto(ruta_de_archivo_traducida, 'w+') as wf:
        wf.escribir(traducido)
    with abierto(ruta_del_mapa_de_traducción, 'w+') as wf:
        wf.escribir(mapa_de_traducción)


def traducir_todo(config, DEST_LANG):
    """
    Translate all files, excluding those defined by the polycodeignore file
    """
    # Load polycodeignore
    ignorar_archivos = []
    if os.camino.isfile(TRADUCIR_IGNORAR_NOMBRE_DE_ARCHIVO):
        with abierto(TRADUCIR_IGNORAR_NOMBRE_DE_ARCHIVO) as f:
            for línea in f:
                ignorar_archivos.adjuntar(línea)

    EXTENSIONES_DE_ARCHIVO_DE_DESTINO = config['target_file_extensions']

    # Begin recursive folder walk in current directory
    caminar_dir = os.camino.abspath('.')
    archivos_de_destino = []
    for raíz, subdivisiones, archivos in os.caminar(caminar_dir):
        nombres de archivo = [os.camino.unirse(raíz, archivo) for archivo in archivos]
        nombres de archivo = [os.camino.relpath(archivo) for archivo in nombres de archivo]
        for ignorar in ignorar_archivos:
            nombres de archivo = [norte for norte in nombres de archivo if not fnmatch(norte, ignorar)]
        archivos_de_destino.ampliar(nombres de archivo)

    # Read current repo language from temp file if it exists. Else, assume that
    # translation has never been run and thus the language is the source lang
    if os.camino.isfile(TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL):
        with abierto(TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL) as f:
            FUENTE_LANG = f.leer()
    else:
        with abierto(TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL, 'w+') as f:
            f.escribir(config['source_lang'])
        FUENTE_LANG = config['source_lang']

    for archivo in archivos_de_destino:
        if os.camino.splitext(archivo)[-1] in EXTENSIONES_DE_ARCHIVO_DE_DESTINO:
            traducir_archivo(config, archivo, FUENTE_LANG, DEST_LANG)

    with abierto(TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL, 'w+') as f:
        f.escribir(DEST_LANG)


def traducir():
    """
    Helper function performing all operations when command line arg 'translate'
    is called. Allows for no argument calling of translation function.
    """
    # Load config file
    if os.camino.isfile(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO):
        with abierto(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO) as f:
            config = json.carga(f)
    else:
        impresión("Error: No config file found!")
        sys.salida()

    DEST_LANG = sys.argv[2]
    traducir_todo(config, DEST_LANG)


def sin traducir():
    """
    Helper function performing all operations when command line arg
    'untranslate' is called. Allows for no argument calling of untranslation
    function.
    """
    # Load config file
    if os.camino.isfile(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO):
        with abierto(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO) as f:
            config = json.carga(f)
    else:
        impresión("Error: No config file found!")
        sys.salida()

    FUENTE_LANG = config['source_lang']
    traducir_todo(config, FUENTE_LANG)


if __nombre__ == '__main__':
    if len(sys.argv) is 1:
        ayuda()
        sys.salida()

    if '--help' in sys.argv:
        ayuda()
        sys.salida()

    # Load config file
    if os.camino.isfile(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO):
        with abierto(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO) as f:
            config = json.carga(f)
    else:
        impresión("Error: No config file found!")
        sys.salida()

    # Create translation cache folder if it does not exist
    if not os.camino.existe(TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT):
        os.makedirs(TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT)

    # Create translation temp file with default language if it does not exist
    if not os.camino.isfile(TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL):
        with abierto(TRADUCIR_NOMBRE_DE_ARCHIVO_TEMPORAL, 'w+') as f:
            f.escribir(config['source_lang'])

    if sys.argv[1] == 'translate':
        traducir()

    if sys.argv[1] == 'untranslate':
        sin traducir()

    # if sys.argv[1] == '--f':
    #     target_file = sys.argv[2]
    #     DEST_LANG = sys.argv[3]
    #     translate_file(config, target_file, DEST_LANG)
