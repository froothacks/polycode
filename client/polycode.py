import os
import sys
import json
from fnmatch import fnmatch
from lib import lib

# Polyglot

TRANSLATE_CONFIG_FILENAME = '.polycode'
TRANSLATE_IGNORE_FILENAME = '.polycodeignore'
TRANSLATE_TEMP_FILENAME = '.polycodetmp'

TRANSLATED_FILES_PATH_TEMPLATE = 'repo-{}/'
TRANSLATE_DICT_FILES_PATH = '.polycodedata/'


def help():
    helptext = """
    Usage: polycode [--help] [Destination Language]

    Examples:
      polycode build ES -> Builds Spanish project version into default lang
      polycode translate ES -> Translates current project into Spanish
      polycode --f targetfile ES -> Translates file 'targetfile' into Spanish
    """
    print(helptext)


def translate_file(config, target_file, SOURCE_LANG, DEST_LANG):
    FUNCTION_CASE = config['function_case']
    CLASS_CASE = config['class_case']

    with open(target_file) as f:
        source = f.read()

    map_file_path = TRANSLATE_DICT_FILES_PATH + '{}.map'.format(target_file)
    map = {}
    if os.path.isfile(map_file_path):
        with open(map_file_path) as f:
            map = f.read()

    result = lib.davidgu.polycode['@dev'](doc=source,
                                  config=json.dumps(config), map=map)
    translated = result['doc']
    translation_map = json.dumps(result['map'])

    # Translations overwrite the translated file
    translated_file_path = target_file
    translation_map_path = map_file_path

    # Write received files
    with open(translated_file_path, 'w+') as wf:
        wf.write(translated)
    with open(translation_map_path, 'w+') as wf:
        wf.write(translation_map)

def translate_all(config, DEST_LANG):
    # Load polycodeignore
    ignore_files = []
    if os.path.isfile(TRANSLATE_IGNORE_FILENAME):
        with open(TRANSLATE_IGNORE_FILENAME) as f:
            for line in f:
                ignore_files.append(line)

    TARGET_FILE_EXTENSIONS = config['target_file_extensions']

    # Begin recursive folder walk in current directory
    walk_dir = os.path.abspath('.')
    target_files = []
    for root, subdirs, files in os.walk(walk_dir):
        filenames = [os.path.join(root, file) for file in files]
        filenames = [os.path.relpath(file) for file in filenames]
        for ignore in ignore_files:
            filenames = [n for n in filenames if not fnmatch(n, ignore)]
        target_files.extend(filenames)

    # The temp file contains the current repo language
    with open(TRANSLATE_TEMP_FILENAME) as f:
        SOURCE_LANG = f.read()

    for file in target_files:
        if os.path.splitext(file)[-1] in TARGET_FILE_EXTENSIONS:
            translate_file(config, file, SOURCE_LANG, DEST_LANG)

    with open(TRANSLATE_TEMP_FILENAME, 'w+') as f:
        f.write(DEST_LANG)


if __name__ == '__main__':
    if len(sys.argv) is 1:
        help()
        sys.exit()

    if '--help' in sys.argv:
        help()
        sys.exit()

    # Load config file
    if os.path.isfile(TRANSLATE_CONFIG_FILENAME):
        with open(TRANSLATE_CONFIG_FILENAME) as f:
            config = json.load(f)
    else:
        print("Error: No config file found!")
        sys.exit()

    # Create translation cache folder if it does not exist
    if not os.path.exists(TRANSLATE_DICT_FILES_PATH):
        os.makedirs(TRANSLATE_DICT_FILES_PATH)

    # Create translation temp file with default language if it does not exist
    if not os.path.isfile(TRANSLATE_TEMP_FILENAME):
        with open(TRANSLATE_TEMP_FILENAME, 'w+') as f:
            f.write(config['source_lang'])

    if sys.argv[1] == 'translate':
        DEST_LANG = sys.argv[2]
        translate_all(config, DEST_LANG)

    if sys.argv[1] == 'build':
        SOURCE_LANG = config['source_lang']
        translate_all(config, SOURCE_LANG)

    # if sys.argv[1] == '--f':
    #     target_file = sys.argv[2]
    #     DEST_LANG = sys.argv[3]
    #     translate_file(config, target_file, DEST_LANG)
