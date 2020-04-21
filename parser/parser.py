import json
import os
import sys

from untar import decompress
from cleanup import cleanit
from loader import loaddb

files = []

if sys.argv[1] != 'single':
    files = decompress().split()
else:
    files.append('./')
    files.append(sys.argv[2])

path = files[0]

for file in files[1:]:
    print("Executing on file " + file)
    file = path + file

    tweets = []
    for line in open(file, 'r'):
        if u'text' in json.loads(line) and json.loads(line)['lang'] == 'en':
            tweets.append(json.loads(line))

    newdic = {}
    newdic['tweets'] = []
    hashtags = []
    for dic in tweets:
        len_tags = len(dic['entities']['hashtags'])
        if len_tags > 0:
            for x in range(0, len_tags):
                hashtags.append(dic['entities']['hashtags'][x]['text'])

        newdic['tweets'].append({
            'text': dic['text'],
            'hashtag': hashtags[:],
            'created_at': dic['created_at'].split()[5],
        })
        del hashtags[:]

    newfile = file + '.txt'

    with open(newfile, 'w') as outfile:
        json.dump(newdic, outfile, indent=2)

    outfile.close()

print("\n")
cleanit(path)

print("\nBeginning upload to database...")
loaddb(path, files)

print("\nSuccess!")
