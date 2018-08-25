import os
import sys
import requests
import json

# Polyglot

TRANSLATE_CONFIG_FILENAME = '.polycode'
TRANSLATE_DATA_FILENAME = '.polycode_data'

def help():
    helptext = """
    Usage: translate [--help] [Destination Language]

    Examples:
      translate build ES -> Builds current project into Spanish
      translate --f targetfile ES -> Translates file 'targetfile' into Spanish
    """
    print(helptext)


if __name__ == '__main__':
    if len(sys.argv) is 1:
        help()
        sys.exit()

    if '--help' in sys.argv:
        help() 
        sys.exit()

    if sys.argv[1] == 'build':
        # Load config file
        if os.path.isfile(TRANSLATE_CONFIG_FILENAME):
            with open(TRANSLATE_CONFIG_FILENAME) as f:
                config = json.load(f)
        else:
            print("Error: No config file found!")
            sys.exit()

        # Check if translate data file exists in current repo
        if os.path.isfile(TRANSLATE_DATA_FILENAME):
            with open(TRANSLATE_DATA_FILENAME) as f:
                translation_file = json.load(f)
        else:
            translation_file = {}

        DEST_LANG = sys.argv[2]
        TARGET_FILE_EXTENSIONS = config['target_file_extensions']

        # Begin recursive folder walk in current directory
        walk_dir = os.path.abspath('.')
        for root, subdirs, files in os.walk(walk_dir):
            for filename in files:
                target_file = os.path.join(root, filename)
                if os.path.splitext(target_file)[-1] in TARGET_FILE_EXTENSIONS:
                    translate_file(target_file, DEST_LANG)
                    print(target_file)

    if sys.argv[1] == '--f':
        target_file = sys.argv[2]
        DEST_LANG = sys.argv[3]
        translate_file(target_file, DEST_LANG)

def translate_file(target_file, DEST_LANG):
    SOURCE_LANG = config['source_lang']
    FUNCTION_CASE = config['function_case']
    CLASS_CASE = config['class_case']

    with open(target_file) as f:
        source = f.read()
        #TODO: Send the source file to be translated
        #TODO: Receive the translated source file
        #TODO: Receive the translation map file
        translated = f.read()
        translation_map = '{}'

        translated_file_name = '{}.{}{}'.format(
            os.path.splitext(target_file)[0], 
            DEST_LANG, 
            os.path.splitext(target_file)[-1])
        translation_map_name = '{}.{}{}.map'.format(
            os.path.splitext(target_file)[0], 
            DEST_LANG, 
            os.path.splitext(target_file)[-1])

        # Write received files
        with open(translated_file_name, 'w+') as wf:
            wf.write(translated)
        with open (translation_map, 'w+') as wf:
            wf.write(translation_map)
