#! python3

# subtitles.py - Search https://www.yify-subtitles.com/
#               Downloads the highest rated subtitle (based on language
#               specified, default is English)
#               Unzips the downloaded zipped file and
#               send the zipped file to trash once extracted.

import sys
from findSubtitles import find_subs

# Implement the ability to search for movie subtitles via command prompt
if len(sys.argv) == 1:
    print('\nType in command prompt to find subtitles:\n')
    print('\t' + '\033[43m' + 'subtitles <movie>' + '\033[0m' + '\n')

elif len(sys.argv) > 1:
    movieName = ' '.join(sys.argv[1:])
    find_subs(movieName)
