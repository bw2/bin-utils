export PS1="\h:\w]$ "

function settitle {  printf "\033]0;%s\007" "$1"; };

PATH=/usr/local/bin:$PATH

# aliases
alias ll='ls -la'
alias gs='gsutil'


# save history on logout
export CUSTOM_HISTFILE="${HOME}/.history_full/$(date -u +%Y/%m/%d.%H.%M.%S)_$$"
mkdir -p ${HOME}/.history_full/$(date -u +%Y/%m/)
touch $CUSTOM_HISTFILE

function search_history() {
    echo "Searching for '$1'"
    grep $1 ~/.history_full/20*/*/*
}

function add_note() {
    echo 'ADD NOTE'
    date | xargs echo -n >> $CUSTOM_HISTFILE
    echo -n ' - NOTE: ' >>$CUSTOM_HISTFILE
    echo $1 >>$CUSTOM_HISTFILE
}

export PROMPT_COMMAND=__prompt_command  # Func to gen PS1 after CMDs

export STARTED=0
function __prompt_command() {
        local EXIT="$?"             # This needs to be first
        red=$(tput setaf 1)    #\e[31m
        green=$(tput setaf 2)    #\e[32m
        yellow=$(tput setaf 3)  #\e[33m
        blue=$(tput setaf 4)    #\e[34m
        purple=$(tput setaf 5)    #\e[35m
        reset=$(tput sgr0)      #\e[0m
        if [[ $STARTED -ne 0 ]]; then
                history -a
                date | xargs echo -n >> $CUSTOM_HISTFILE
                echo -n ' - ' >>$CUSTOM_HISTFILE
                LAST_CMD=`tail -n 1 $HISTFILE`
                PRINT_WD=$PWD
                if [[ $EXIT -eq 0 ]] && [[ $LAST_CMD == cd* ]]; then
                    PRINT_WD=$OLDPWD
                fi
                echo $PRINT_WD | xargs echo -n >>$CUSTOM_HISTFILE
                echo -n ' - ' >>$CUSTOM_HISTFILE
                echo -n $EXIT >>$CUSTOM_HISTFILE
                echo -n ' - ' >>$CUSTOM_HISTFILE
                echo $LAST_CMD >>$CUSTOM_HISTFILE
		#echo command $LAST_CMD saved to $CUSTOM_HISTFILE
        fi
        export STARTED=1
        PS1='\[$blue\]\h:\[$blue\]\w \$ '
}

