import os
import sys
import json
from fnmatch import fnmatch
from lib import lib

# Polyglot

TRANSLATE_CONFIG_FILENAME = '.polycode'
TRANSLATE_IGNORE_FILENAME = '.polycodeignore'

TRANSLATED_FILES_PATH_TEMPLATE = 'repo-{}/'
TRANSLATE_DICT_FILES_PATH = '.polycodedata/'


def help():
    helptext = """
    Usage: translate [--help] [Destination Language]

    Examples:
      translate build ES -> Builds current project into Spanish
      translate --f targetfile ES -> Translates file 'targetfile' into Spanish
    """
    print(helptext)


def translate_file(config, target_file, DEST_LANG):
    SOURCE_LANG = config['source_lang']
    FUNCTION_CASE = config['function_case']
    CLASS_CASE = config['class_case']

    with open(target_file) as f:
        source = f.read()
    with open(TRANSLATE_DICT_FILES_PATH + '{}.{}{}.map'.format(
                os.path.splitext(target_file)[0],
                DEST_LANG,
                os.path.splitext(target_file)[-1])) as f:
                map = f.read()

    result = lib.davidgu.polycode(doc=source,
                                  config=json.dumps(config), map=map)
    translated = result['doc']
    translation_map = json.dumps(result['map'])

    # If the file is being translated back to its original language,
    # write a file with no language extension
    if DEST_LANG == config['source_lang']:
        translated_file_name = '{}{}'.format(
            os.path.splitext(os.path.splitext(target_file)[0])[0],
            os.path.splitext(target_file)[-1])
        translated_file_path = translated_file_name
    else:
        translated_file_name = '{}.{}{}'.format(
            os.path.splitext(target_file)[0],
            DEST_LANG,
            os.path.splitext(target_file)[-1])
        translated_file_path = TRANSLATED_FILES_PATH_TEMPLATE.format(
            DEST_LANG) + translated_file_name
    translation_map_name = '{}.{}{}.map'.format(
        os.path.splitext(target_file)[0],
        DEST_LANG,
        os.path.splitext(target_file)[-1])
    print(translation_map_name)
    translation_map_path = TRANSLATE_DICT_FILES_PATH + translation_map_name

    # Write received files
    with open(translated_file_path, 'w+') as wf:
        wf.write(translated)
    with open(translation_map_path, 'w+') as wf:
        wf.write(translation_map)


if __name__ == '__main__':
    if len(sys.argv) is 1:
        help()
        sys.exit()

    if '--help' in sys.argv:
        help()
        sys.exit()

    # Create translation cache folder if it does not exist
    if not os.path.exists(TRANSLATE_DICT_FILES_PATH):
        os.makedirs(TRANSLATE_DICT_FILES_PATH)

    if sys.argv[1] == 'build':
        # Load config file
        if os.path.isfile(TRANSLATE_CONFIG_FILENAME):
            with open(TRANSLATE_CONFIG_FILENAME) as f:
                config = json.load(f)
        else:
            print("Error: No config file found!")
            sys.exit()

        # Load polycodeignore
        ignore_files = []
        if os.path.isfile(TRANSLATE_IGNORE_FILENAME):
            with open(TRANSLATE_IGNORE_FILENAME) as f:
                for line in f:
                    ignore_files.append(line)

        DEST_LANG = sys.argv[2]
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

        for file in target_files:
            if os.path.splitext(file)[-1] in TARGET_FILE_EXTENSIONS:
                translate_file(config, file, DEST_LANG)

    if sys.argv[1] == '--f':
        target_file = sys.argv[2]
        DEST_LANG = sys.argv[3]
        translate_file(config, target_file, DEST_LANG)
