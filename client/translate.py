import os
import sys
import requests
import json

# Polyglot

TRANSLATE_CONFIG_FILENAME = '.polyglot'
TRANSLATE_DATA_FILENAME = '.polyglot_data'

def help():
    helptext = """
    Usage: translate [--help] [Destination Language]
    """


if __name__ == '__main__':
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

    # Check if translate data file exists in current repo
    if os.path.isfile(TRANSLATE_DATA_FILENAME):
        with open(TRANSLATE_DATA_FILENAME) as f:
            translation_file = json.load(f)
    else:
        translation_file = {}

    TARGET_FILE_EXTENSIONS = config['target_file_extensions']
    SOURCE_LANG = config['source_lang']
    DEST_LANG = sys.argv[1]

    # Begin recursive folder walk in current directory
    walk_dir = os.path.abspath('.')
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            target_file = os.path.join(dirpath,filename)
            if os.path.splittext(target_file)[-1] in TARGET_FILE_EXTENSIONS:
                with open(target_file) as f:
                    source = f.read()
                    #TODO: Send the source file to be translated
                    #TODO: Receive the translated source file
                    #TODO: Receive the translation map file
                    translated = f.read()
                    translation_map = '{}'

                    translated_file_name = '{}.{}{}'.format(
                        os.path.splittext(target_file)[0], 
                        DEST_LANG, 
                        os.path.splittext(target_file)[-1])
                    translation_map_name = '{}.{}{}.map'.format(
                        os.path.splittext(target_file)[0], 
                        DEST_LANG, 
                        os.path.splittext(target_file)[-1])

                    # Write received files
                    with open(translated_file_name, 'w+') as wf:
                        wf.write(translated)
                    with open (translation_map, 'w+') as wf:
                        wf.write(translation_map)




                    
