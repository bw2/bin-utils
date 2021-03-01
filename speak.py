#!/usr/bin/python3

# MacOSX 'say' command docs: https://ss64.com/osx/say.html

"""
Custom text-to-speach for MacOSX

Adding voices:

1. Open System Preferences > Accessibility > Speech 
2. Select system voices: Allison (or Ava) for English, Milena for Russian, Carmit for Hebrew

Creating commands:

"speak" command:

1. Open Automator > Select New > Quick Action
2. Workflow receives current "Automatic (text)" in "any application"
3. Add a New Text File step:
     File format: Same as input text
     Save as: say.txt
     Where: bin-utils dir  (replacing existing files)
4. Add a Run Shell Script step:
     Shell: /bin/bash    Pass Input: as arguments
     /Users/weisburd/bin/bin-utils/speak.py -v Ava
5. File > Export.. > enter workflow name > Save 
6. System Preferences > Keyboard Shortcuts > Service > speak > Command:option:+


"stop_speaking" command:

1. Open Automator > Select New > Quick Action
2. Add a Run Bash Script step:
if pgrep say; then
   pkill -f say
fi

3. System Preferences > Keyboard Shortcuts > Service > stop_speaking > Command:option:-


Setting up commands:

1. cd ~/bin/bin-utils/speak_quick_actions
2. open speak.workflow   # confirm prompt to install 
   open speak_russian.workflow
   open stop_speaking.workflow
3. System Preferences > Keyboard Shortcuts > Service > start_speaking > command-option-plus
                                                        stop_speaking > command-option-minus
                                                        speak_russian > command-option-9
                                                         speak_hebrew > command-option-8


"""

import os
import sys

path = os.path.expanduser("~/bin/bin-utils/say.txt")
with open(path, "rt") as f:
    contents = f.read()

# custom pronunciation - case-sensitive
contents = contents.replace('ASOs', "a. s. o's. ")
contents = contents.replace('ASO', "a. s. o. ")

# custom pronunciation - case-insensitive
contents = contents.lower()
for t in ["rnaseq", "rna-seq", "rna seq"]:
    contents = contents.replace(t, "rna-seek")
contents = contents.replace('paradigm', "paradime" )

with open(path, "wt") as f:
    f.write(contents)

speech_rate = 200  # -r range: 90 to 600+ words-per-minute
if "Milena" in sys.argv[1:]:
    speech_rate = 150
elif "Carmit" in sys.argv[1:]:
    speech_rate = 120    

os.system(f"say -r {speech_rate} " + " ".join(sys.argv[1:]) + " -f " + path)  

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
