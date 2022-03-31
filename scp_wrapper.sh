#!/bin/sh

function scp
{
    echo 'Hello'
    typeset argv="$@"
    typeset target="${argv[-1]}"

    if [[ -e "$target" ]]; then
        echo 'Target file exists, refusing to overwrite' >&2
        return 1
    fi

    command scp "$@"
}
