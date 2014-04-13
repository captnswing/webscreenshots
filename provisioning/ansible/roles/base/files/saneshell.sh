#--------
# pager
#--------
alias more=less
export PAGER=less
export LESS="-i -M -w -R -S -X"

#--------
# process list
#--------
function psa () {
    if [ $1 ]; then
        ps auxwwww | grep -v grep | grep -i $1
    else
        ps auxwwww
    fi
}

#--------
# history
#--------
export HISTSIZE=5000
export HISTCONTROL="erasedups"
shopt -s histappend
export PROMPT_COMMAND="history -a"
export HISTIGNORE="l:ls -la:l[lhs]:h:..:...:cd:[bf]g:exit"

function h () {
    if [ $1 ]; then
        history | grep -i $1 | tail -250 | grep -i $1
    else
        history | tail -250
    fi
}
