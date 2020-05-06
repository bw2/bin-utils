#!/usr/bin/python3

# MacOSX 'say' command docs: https://ss64.com/osx/say.html

"""
Custom text-to-speach for MacOSX

"speak" command:

1. Open Automator > Select New > Quick Action
2. Workflow receives current "Automatic (text)" in "any application"
3. Add a New Text File step:
     File format: Same as input text
     Save as: say.txt
     Where: bin-utils dir  (replacing existing files)
4. Add a Run Bash Script step:
     Shell: /bin/bash    Pass Input: as arguments
     /Users/weisburd/bin/bin-utils/speak.py

5. System > Preferences > Keyboard Shortcuts > Service > speak > Command:option:+


"stop_speaking" command:

1. Open Automator > Select New > Quick Action
2. Add a Run Bash Script step:
if pgrep say; then
   pkill -f say
fi

3. System > Preferences > Keyboard Shortcuts > Service > stop_speaking > Command:option:-

"""

import os

path = os.path.expanduser("~/bin/bin-utils/say.txt")
with open(path, "rt") as f:
    contents = f.read()

# custom pronunciation
contents = contents.lower()
for t in ["rnaseq", "rna-seq", "rna seq"]:
    contents = contents.replace(t, "rna-seek")
    
with open(path, "wt") as f:
    f.write(contents)

os.system("say -v Ava -f " + path)
