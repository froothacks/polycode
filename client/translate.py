import os
import sys
import json
from fnmatch import fnmatch
from lib import lib

# Polyglot

TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO = '.polycode'
TRADUCIR_IGNORAR_NOMBRE_DE_ARCHIVO = '.polycodeignore'

PLANTILLA_DE_RUTA_DE_ARCHIVOS_TRADUCIDOS = 'repo-{}/'
TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT = '.polycodedata/'


def ayuda():
    texto de ayuda = """
    Usage: translate [--help] [Destination Language]

    Examples:
      translate build ES -> Builds current project into Spanish
      translate --f targetfile ES -> Translates file 'targetfile' into Spanish
    """
    impresión(texto de ayuda)


def traducir_archivo(config, archivo_de_destino, DEST_LANG):
    FUENTE_LANG = config['source_lang']
    FUNDA_DE_FUNCIÓN = config['function_case']
    CASO_DE_CLASE = config['class_case']

    with abierto(archivo_de_destino) as f:
        fuente = f.leer()
    with abierto(TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT + '{}.{}{}.map'.formato(
                os.camino.splitext(archivo_de_destino)[0],
                DEST_LANG,
                os.camino.splitext(archivo_de_destino)[-1])) as f:
                mapa = f.leer()

    resultado = lib.davidgu.polycode(doc=fuente,
                                  config=json.deshecho(config), mapa=mapa)
    traducido = resultado['doc']
    mapa_de_traducción = json.deshecho(resultado['map'])

    # If the file is being translated back to its original language,
    # write a file with no language extension
    if DEST_LANG == config['source_lang']:
        nombre_de_archivo_traducido = '{}{}'.formato(
            os.camino.splitext(os.camino.splitext(archivo_de_destino)[0])[0],
            os.camino.splitext(archivo_de_destino)[-1])
        ruta_de_archivo_traducida = nombre_de_archivo_traducido
    else:
        nombre_de_archivo_traducido = '{}.{}{}'.formato(
            os.camino.splitext(archivo_de_destino)[0],
            DEST_LANG,
            os.camino.splitext(archivo_de_destino)[-1])
        ruta_de_archivo_traducida = PLANTILLA_DE_RUTA_DE_ARCHIVOS_TRADUCIDOS.formato(
            DEST_LANG) + nombre_de_archivo_traducido
    nombre_del_mapa_de_traducción = '{}.{}{}.map'.formato(
        os.camino.splitext(archivo_de_destino)[0],
        DEST_LANG,
        os.camino.splitext(archivo_de_destino)[-1])
    impresión(nombre_del_mapa_de_traducción)
    ruta_del_mapa_de_traducción = TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT + nombre_del_mapa_de_traducción

    # Write received files
    with abierto(ruta_de_archivo_traducida, 'w+') as wf:
        wf.escribir(traducido)
    with abierto(ruta_del_mapa_de_traducción, 'w+') as wf:
        wf.escribir(mapa_de_traducción)


if __nombre__ == '__main__':
    if len(sys.argv) is 1:
        ayuda()
        sys.salida()

    if '--help' in sys.argv:
        ayuda()
        sys.salida()

    # Create translation cache folder if it does not exist
    if not os.camino.existe(TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT):
        os.makedirs(TRADUCIR_LA_RUTA_DE_LOS_ARCHIVOS_DICT)

    if sys.argv[1] == 'build':
        # Load config file
        if os.camino.isfile(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO):
            with abierto(TRADUCIR_CONFIG_NOMBRE_DE_ARCHIVO) as f:
                config = json.carga(f)
        else:
            impresión("Error: No config file found!")
            sys.salida()

        # Load polycodeignore
        ignorar_archivos = []
        if os.camino.isfile(TRADUCIR_IGNORAR_NOMBRE_DE_ARCHIVO):
            with abierto(TRADUCIR_IGNORAR_NOMBRE_DE_ARCHIVO) as f:
                for línea in f:
                    ignorar_archivos.adjuntar(línea)

        DEST_LANG = sys.argv[2]
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

        for archivo in archivos_de_destino:
            if os.camino.splitext(archivo)[-1] in EXTENSIONES_DE_ARCHIVO_DE_DESTINO:
                traducir_archivo(config, archivo, DEST_LANG)

    if sys.argv[1] == '--f':
        archivo_de_destino = sys.argv[2]
        DEST_LANG = sys.argv[3]
        traducir_archivo(config, archivo_de_destino, DEST_LANG)
