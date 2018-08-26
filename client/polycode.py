import os
import sys
import json
import argparse
import codecs
from fnmatch import fnmatch
import requests
# from lib import lib as lib_inst

# Polyglot

TRANSLATE_CONFIG_FILENAME = '.polycode'
TRANSLATE_IGNORE_FILENAME = '.polycodeignore'
TRANSLATE_TEMP_FILENAME = '.polycodetmp'
TRANSLATE_PERSONAL_CONFIG_FILEPATH = '~/.polycode'

TRANSLATED_FILES_PATH_TEMPLATE = 'repo-{}/'
TRANSLATE_DICT_FILES_PATH = '.polycodedata/'
SERVER_URL = 'https://davidgu.stdlib.com/polycode@dev'

def fake_backend(payload):
    # print(payload)
    return json.dumps({
        'doc':'This is a source code file that would be translated',
        'map':{
            "languages": ["EN", "FR", "ZH"],
            "tokens": [
                ["banana", "banane", "香蕉"],
                ["fish", "poisson", "鱼"],
                ["banana_fish", "banane_poisson", "香蕉_鱼"]
            ]
        }
    })


def help():
    helptext = """
    Usage: polycode [--help] [Destination Language]

    Examples:
      polycode untranslate
      polycode translate ES -> Translates current project into Spanish
      polycode --f targetfile ES -> Translates file 'targetfile' into Spanish
    """
    print(helptext)


def translate_file(config, target_file, SOURCE_LANG, DEST_LANG):
    """
    Translate a specific file
    """

    with codecs.open(target_file, "r", "utf-8") as f:
        source = f.read()

    map_file_path = TRANSLATE_DICT_FILES_PATH + '{}.map'.format(target_file)
    map = {}
    if os.path.isfile(map_file_path):
        with open(map_file_path) as f:
            map = f.read()
            map = json.loads(map)

    # result = lib_inst.davidgu.polycode['@dev'](source, config, map)

    fextension = os.path.splitext(target_file)[1]

    payload = {'doc': source, 'from': SOURCE_LANG, 
        'to': DEST_LANG, 'map': json.dumps(map), 'ext':fextension}
    # print(payload)
    req = requests.get(SERVER_URL, params=payload)
    # print(req.url)
    result = json.loads(req.text)

    # Use fake backend for testing
    # result = json.loads(fake_backend(payload))

    translated = result['doc']
    translation_map = json.dumps(result['map'])

    # Translations overwrite the translated file
    translated_file_path = target_file
    translation_map_path = map_file_path

    # Write received files
    with codecs.open(translated_file_path, "w+", "utf-8") as wf:
        wf.write(translated)

    # Create directories for translation maps if they do not exist
    if not os.path.exists(os.path.dirname(translation_map_path)):
        try:
            os.makedirs(os.path.dirname(translation_map_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with codecs.open(translation_map_path, "w+", "utf-8") as wf:
        wf.write(translation_map)


def translate_all(config, DEST_LANG, additional_ignores=[]):
    """
    Translate all files, excluding those defined by the polycodeignore file
    """
    # Load polycodeignore
    ignore_files = additional_ignores
    if os.path.isfile(TRANSLATE_IGNORE_FILENAME):
        with open(TRANSLATE_IGNORE_FILENAME) as f:
            for line in f:
                ignore_files.append(line.strip())
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

    # Read current repo language from temp file if it exists. Else, assume that
    # translation has never been run and thus the language is the source lang
    if os.path.isfile(TRANSLATE_TEMP_FILENAME):
        with open(TRANSLATE_TEMP_FILENAME) as f:
            tmp_data = json.loads(f.read())
            SOURCE_LANG = tmp_data['current_lang']
    else:
        with open(TRANSLATE_TEMP_FILENAME, 'w+') as f:
            tmp_data = {'current_lang':config['source_lang']}
            f.write(json.dumps(tmp_data))
        SOURCE_LANG = config['source_lang']

    for file in target_files:
        if os.path.splitext(file)[-1] in TARGET_FILE_EXTENSIONS:
            translate_file(config, file, SOURCE_LANG, DEST_LANG)
            print(file)

    with open(TRANSLATE_TEMP_FILENAME, 'r+') as f:
        tmp_data = json.loads(f.read())
        tmp_data['current_lang'] = DEST_LANG
    with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
        f.write(json.dumps(tmp_data))

def main():
    # Load project config file
    if os.path.isfile(TRANSLATE_CONFIG_FILENAME):
        with open(TRANSLATE_CONFIG_FILENAME) as f:
            config = json.load(f)
    else:
        print("Error: No config file found!")
        sys.exit()

    # Load personal config file
    if os.path.isfile(os.path.expanduser(TRANSLATE_PERSONAL_CONFIG_FILEPATH)):
        with open(os.path.expanduser(TRANSLATE_PERSONAL_CONFIG_FILEPATH)) as f:
            pconfig = json.load(f)
    else:
        print("Error: No personal config file found at {} !".format(
            os.path.expanduser(TRANSLATE_PERSONAL_CONFIG_FILEPATH)))
        sys.exit()

    # Create translation cache folder if it does not exist
    if not os.path.exists(TRANSLATE_DICT_FILES_PATH):
        os.makedirs(TRANSLATE_DICT_FILES_PATH)

    # Create translation temp file with default language if it does not exist
    if not os.path.isfile(TRANSLATE_TEMP_FILENAME):
        with open(TRANSLATE_TEMP_FILENAME, 'w+') as f:
            tmp_data = {'current_lang':config['source_lang']}
            f.write(json.dumps(tmp_data))

    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['translate', 'untranslate',
        'commit', 'pull', 'define', 'definition', 'run', 'watch'])
    parser.add_argument('-s', '--single-file', 
        type=str, help='Translate a single file instead of the whole project')
    parser.add_argument('-l', '--language', type=str,
        help='Specify the language to translate to.')
    parser.add_argument('-w', '--word', type=str, 
        help='Define a word to define or get a definition of.')
    parser.add_argument('-d', '--definition', type=str, 
        help='The new value of the specified word.')
    args = parser.parse_args()

    if args.command == 'translate':
        OUTPUT_LANG = pconfig['output_lang']
        # If a specific output language is specified, use it
        if args.language:
            OUTPUT_LANG = args.language
        translate_file(config, args.single_file, config['source_lang'],
            OUTPUT_LANG)

        # If a single file is specified, apply translation to that file
        if args.single_file:
            # Remember translated file in temporary file
            with open(TRANSLATE_TEMP_FILENAME, 'r') as f:
                tmp_data = json.loads(f.read())
                if 'single_translated_files' in tmp_data:
                    # Only add the file to the list of singly translated files if it is not already in there
                    if args.single_file not in [x.split(' ')[0] for x in tmp_data['single_translated_files']]:
                        tmp_data['single_translated_files'].append(
                            '{} {}'.format(args.single_file, OUTPUT_LANG))
                else:
                    tmp_data['single_translated_files'] = [
                        '{} {}'.format(args.single_file, OUTPUT_LANG)]
            with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
                f.write(json.dumps(tmp_data))
        else:
            translate_all(config, OUTPUT_LANG)
    
    # Untranslate reverts all translated files to the project source lang
    if args.command == 'untranslate':
        # Accept single file flag to untranslate a specific file
        # TODO:Give an error message if the specified file is not currently
        # translated
        # Remember translated file in temporary file

        with open(TRANSLATE_TEMP_FILENAME, 'r+') as f:
            tmp_data = json.loads(f.read())
            # If the current state of the entire repo is translated, store 
            # the updated file under the single translated files. Otherwise,
            # if the untranslated file is an individually translated file,
            # remove it from the list of single translated files.

            # flow: Check whole repo state -> Check individual file state ->
            # if the whole repo is not translated and the file is not
            # individually translated, fail with error message.
            # If the whole repo is translated and the file is individually
            # translated to the source lang, fail with an error message

        # Get the singly translated files and filenames
        st_files = []
        if 'single_translated_files' in tmp_data:
            st_files = tmp_data['single_translated_files']
        st_filenames = [x.split(' ')[0] for x in st_files]

        # Check whole repo translation state
        if tmp_data['current_lang'] != config['source_lang']:
            # The whole repo has been translated


            # Check if a single file is specified
            if args.single_file:
                # If the single file was specially translated, get it's current
                # language from the temp file
                
                if args.single_file in st_filenames:
                    for file in st_files:
                        filename, file_lang = file.split(' ')
                        if args.single_file == filename:
                            file_current_lang = file_lang 

                    # Untranslate that specific file and remove it from the 
                    # single_translated_files list
                    translate_file(config, filename, file_lang,
                        config['source_lang'])

                    for idx in range(len(st_files)):
                        if st_files[idx].split(' ')[0] == args.single_file:
                            st_files.remove(idx)
                            tmp_data['single_translated_files'] = st_files
                            
                    with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
                        f.write(json.dumps(tmp_data))
                
                else:
                    # Untranslate that specific file and mark it in the
                    # single_translated_files list
                    translate_file(config, args.single_file, tmp_data['current_lang'],
                        config['source_lang'])
                    st_files.append('{} {}'.format(
                        args.single_file, config['source_lang']))
                    tmp_data['single_translated_files'] = st_files
                    with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
                        f.write(json.dumps(tmp_data))

            else:
                # Untranslate every file that is not found in the
                # single_translated_files list from the 'current_lang' to the
                # 'source_lang'. Pass in single_translated_files list as 
                # additional ignores
                translate_all(config, config['source_lang'], 
                    st_filenames)

                # Untranslate every file that is found in the
                # single_translated_files list from their current lang to the
                # 'source_lang'
                for file in st_files:
                    filename, file_current_lang = file.split(' ')
                    if file_current_lang != config['source_lang']:
                        translate_file(config, filename, file_current_lang,
                            config['source_lang'])

                # Clear the list of specially translated files
                tmp_data['single_translated_files'] = []
                # Change the repo language back to the source
                tmp_data['current_lang'] = config['source_lang']
                with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
                    f.write(json.dumps(tmp_data))
        else:
            # The whole repo has not yet been translated.

            # Check if a single file is specified
            if args.single_file:
                # Since the whole repo is not yet translated, I must search the
                # list of singly translated files to see if my single file is
                # in there. If it is not, I return an error since the file has
                # not yet been translated
                if args.single_file in st_filenames:
                    for file in st_files:
                        filename, file_lang = file.split(' ')
                        if args.single_file == filename:
                            file_current_lang = file_lang 
                    # Untranslate that specific file and remove it from the 
                    # single_translated_files list
                    translate_file(config, filename, file_lang,
                        config['source_lang'])

                    for idx in range(len(st_files)):
                        if st_files[idx].split(' ')[0] == args.single_file:
                            st_files.pop(idx)
                            tmp_data['single_translated_files'] = st_files
                            
                    with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
                        f.write(json.dumps(tmp_data))
                else:
                    print('Error: Target file has not yet been translated')
                    sys.exit()
            
            else:
                # Untranslate every file that is found in the
                # single_translated_files list from their current lang to the
                # 'source_lang'
                for file in st_files:
                    filename, file_current_lang = file.split(' ')
                    translate_file(config, filename, file_current_lang,
                        config['source_lang'])

                # Clear the list of specially translated files
                tmp_data['single_translated_files'] = []
                with open(TRANSLATE_TEMP_FILENAME, 'w') as f:
                    f.write(json.dumps(tmp_data))

    if args.command == 'commit':
        pass

    if args.command == 'pull':
        pass

    if args.command == 'define':
        # Doesn't handle invalid args
        word = args.word
        definition = args.definition
        file = args.single_file
        from_lang = config['source_lang']
        to_lang = args.language if args.language else pconfig['output_lang']

        map_file_path = TRANSLATE_DICT_FILES_PATH + '{}.map'.format(file)
        dictionary_path = map_file_path
        json_data = json.loads(open(dictionary_path).read())
        dictionary = json_data['tokens']
        languages = json_data['languages']

        # does not handle translating to unsupported languages
        to_lang_idx = languages.index(to_lang)
        from_lang_idx = languages.index(from_lang)
        found = False
        for i in range(len(dictionary)):
            if found:
                continue
            if dictionary[i][from_lang_idx] == word:
                dictionary[i][to_lang_idx] = definition
                found = True

        dict_file = open(dictionary_path, 'w')
        dict_file.write(
            json.dumps({
                'languages': languages,
                'tokens': dictionary
            }, indent=2, ensure_ascii=False)  # ascii false to prevent unicode escape characters
        )

    if args.command == 'definition':
        word = args.word
        file = args.single_file
        from_lang = config['source_lang']
        to_lang = args.language if args.language else pconfig['output_lang']

        map_file_path = TRANSLATE_DICT_FILES_PATH + '{}.map'.format(file)
        dictionary_path = map_file_path
        json_data = json.loads(open(dictionary_path).read())
        dictionary = json_data['tokens']
        languages = json_data['languages']

        to_lang_idx = languages.index(to_lang)
        from_lang_idx = languages.index(from_lang)
        found = False
        for entry in dictionary:
            if found:
                continue
            if entry[from_lang_idx] == word:
                print("Word '%s' in '%s' is '%s'" % (word, to_lang, entry[to_lang_idx]))
                found = True

    if args.command == 'run':
        pass

    if args.command == 'watch':
        pass

if __name__ == '__main__':
    main()