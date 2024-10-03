# Migrate files from Godot to Redot

import fnmatch
import os
import sys
import codecs
#import threading

encoding = 'utf-8'
defaultInputDirectory = '.'
defaultOutputDirectory = '_migrated'
defaultIncludeUnimplemented = False

# Mappings that will currently lead to nowhere. Can be treated as a todo list.
mappings_unimplemented = [
    ('https://docs.godotengine.org', 'https://docs.redotengine.org'),
    ('https://godotengine.org', 'https://redotengine.org'),
    ('https://hosted.weblate.org/projects/godot-engine/godot-docs', 'https://hosted.weblate.org/projects/redot-engine/redot-docs'),
    ('https://hosted.weblate.org/engage/godot-engine/', 'https://hosted.weblate.org/engage/redot-engine/'),
    ('https://chat.godotengine.org/', 'https://chat.redotengine.org/'),
    ('https://nightly.link/godotengine/godot-docs/workflows/build_offline_docs/master/godot', 'https://nightly.link/redotengine/redot-docs/workflows/build_offline_docs/master/redot'),
    ('https://editor.godotengine.org', 'https://editor.redotengine.org'),
    ('https://store.steampowered.com/app/404790/Godot_Engine/', 'https://store.steampowered.com/app/TODO'),
    ('https://flathub.org/apps/details/org.godotengine.Godot', 'https://flathub.org/apps/details/org.redotengine.Redot'),
    ('https://forum.godotengine.org/', 'https://forum.redotengine.org/'),
    ('https://godot.foundation', 'https://redot.foundation'),
    ('GodotEngine.epub', 'RedotEngine.epub'),
    ('godotengine.org/license', 'redotengine.org/license'),
    ('AsGodotDictionary', 'AsRedotDictionary'),
    ('GODOT_', 'REDOT_'),
    ('-godot-', '-redot-'),
    ('project.godot', 'project.redot'),
    ('Godot.Collections', 'Redot.Collections'),
    ('"Godot"', '"Redot"'),
    ('.godot/', '.redot/'),
    ('.godot.', '.redot.'),
    ('APPDATA%\\Godot\\', 'APPDATA%\\Redot\\'),
    ('AppData%\\Godot\\', 'AppData%\\Redot\\'),
    ('Caches/Godot/', 'Caches/Redot/'),
    ('cache/godot/', 'cache/redot'),
    ('Support/Godot/', 'Support/Redot'),
    ('config/godot/', 'config/redot'),
    ('share/godot/', 'share/redot'),
    (' godot_', ' redot_'),
    ('org.godotengine.Godot', 'org.redotengine.Redot'),
    ('godot-ios-plugins', 'redot-ios-plugins'),
    ('godot-syntax-themes', 'redot-syntax-themes'),
    ('godot_skin', 'redot_skin'),
    ('godot_scene_node', 'redot_scene_node'),
    ('``godot', '``redot'),
    ('>/Godot/', '>/Redot/'),
    ('``.godot``', '``.redot``'),
    ('/godot.', '/redot.'),
    ('', ''),
    ('', ''),
]

# Mappings that should work on first migration
mappings = [
    ('https://github.com/godotengine/godot-docs/issues', 'https://github.com/redot-engine/redot-docs/issues'),
    ('https://github.com/godotengine/godot/blob/master', 'https://github.com/redot-engine/redot/blob/master'),
    ('https://raw.githubusercontent.com/godotengine/godot/master', 'https://raw.githubusercontent.com/redot-engine/redot/master'),
    ('https://github.com/godotengine/godot-demo-projects', 'https://github.com/redot-engine/redot-demo-projects'),
    ('https://discord.gg/bdcfAYM4W9', 'https://discord.gg/redot'),
    ('https://github.com/godotengine/godot', 'https://github.com/redotengine/redot'),
    ('https://github.com/godotengine/godot-proposals', 'https://github.com/redot-engine/redot-proposals'),
    ('https://raw.githubusercontent.com/godotengine/godot-docs', 'https://raw.githubusercontent.com/redot-engine/redot-docs'),
    ('https://github.com/godotengine/', 'https://github.com/redot-engine/'),
    ('GODOT_COPYRIGHT.txt', 'REDOT_COPYRIGHT.txt'),
    ('/bin/godot', '/bin/redot'),
    ('/Applications/Godot.app', '/Applications/Redot.app'),
    ('highlight=Godot', 'highlight=Redot'),
    ('/godot_', '/redot_'),
    ('_godot_', '_redot_'),
    ('``godot``', '``redot``'),
    ('Godot ', 'Redot '),
    (' Godot', ' Redot'),
    (' Godot.', ' Redot.'),
    (' Godot?', ' Redot?'),
    ('Godot\'', ' Redot\''),
    ('Godot,', 'Redot,'),
    ('Godot:', 'Redot:'),
    (' godot ', ' redot '),
    ('', ''),
    ('', ''),
    ('', ''),
    ('', ''),
]

filename_mappings = [
    ('godot', 'redot'),
]

# force stdout encoding so it won't fail on print statements
if (sys.stdout.encoding != encoding):
    sys.stdout = codecs.getwriter(encoding)(sys.stdout.buffer, 'strict')
    sys.stdout.encoding = encoding

print(f"Simple rst migrator. Uses str.replace to map from Godot to Redot.")
print(f"Usage: py migrate.py [inputDir] [outputDir] [includeUnimplemented], example: py migrate.py . _mymigration True")
print(f"Author: Craptain @Craptain on X")
print(f"Stdout encoding: {sys.stdout.encoding}")

def migrate(inputDirectory, outputDirectory, includeUnimplemented):
    outputsig = os.path.join('.', outputDirectory)
    print(f"Input directory: {inputDirectory}, output directory: {outputDirectory}, include unimplemented: {includeUnimplemented}")
    for root, dirs, files in os.walk(inputDirectory):
        # ignore output path
        if (root.startswith(outputsig)):
            continue

        items = fnmatch.filter(files, "*.rst")
        if (len(items) > 0):
            for item in items:
                convertFile(root, item, outputDirectory, includeUnimplemented)

def convertFile(root, filename, outputDirectory, includeUnimplemented):
    inputName = os.path.join(root, filename)
    outputName = os.path.join('.', outputDirectory, inputName.replace('.\\', '').replace('./', ''))

    for mapping in filename_mappings:
        search, replace = mapping
        outputName = outputName.replace(search, replace)

    print(f'Processing {inputName} to {outputName}')
    with open(inputName, mode = 'r', encoding = encoding) as input: 
        try: 
            data = input.read()

            if (includeUnimplemented):
                for mapping in mappings_unimplemented:
                    search, replace = mapping
                    if (search != ''):
                        data = data.replace(search, replace)

            for mapping in mappings:
                search, replace = mapping
                if (search != ''):
                    data = data.replace(search, replace)

            dirname = os.path.dirname(outputName)
            try:
                os.makedirs(dirname)
            except FileExistsError:
                pass
            with open(outputName, mode = 'w', encoding = encoding) as output:
                output.write(data)
            
        except UnicodeEncodeError as err:
            print(inputName + ": Unicode encoding failure " + err.reason)
    

inputDir = defaultInputDirectory
outputDir = defaultOutputDirectory
includeUnimplemented = defaultIncludeUnimplemented
if (len(sys.argv) > 1):
    inputDir = sys.argv[1]
if (len(sys.argv) > 2):
    outputDir = sys.argv[2]
if (len(sys.argv) > 3):
    includeUnimplemented = sys.argv[3]

migrate(inputDir, outputDir, includeUnimplemented)