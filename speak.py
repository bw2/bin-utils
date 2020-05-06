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

os.system("say -r 250 -v Ava -f " + path)  # -r range: 90 to 600+ words-per-minute


"""
Voices: (from say --voices=?)

Alex                en_US    # Most people recognize me by my voice.
Allison             en_US    # Hello, my name is Allison. I am an American-English voice.
Ava                 en_US    # Hello, my name is Ava. I am an American-English voice.
Daniel              en_GB    # Hello, my name is Daniel. I am a British-English voice.
Fiona               en-scotland # Hello, my name is Fiona. I am a Scottish-English voice.
Karen               en_AU    # Hello, my name is Karen. I am an Australian-English voice.
Veena               en_IN    # Hello, my name is Veena. I am an Indian-English voice.
Tessa               en_ZA    # Hello, my name is Tessa. I am a South African-English voice.
Carmit              he_IL    # שלום. קוראים לי כרמית, ואני קול בשפה העברית.
Milena              ru_RU    # Здравствуйте, меня зовут Milena. Я – русский голос системы.
Yuri                ru_RU    # Здравствуйте, меня зовут Yuri. Я – русский голос системы.

"""
