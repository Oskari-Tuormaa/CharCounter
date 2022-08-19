#!/bin/bash

main() {
    if [ -x "$(command -v python)" ]; then
        if [ -z "$1" ]; then
            read -e -p "Please enter path to main .tex file: " -r test
        else
            test="$1"
        fi

        if [ -z "$test" ]; then
            echo "No path specified."
            return -1
        fi

        if ! [ -f "$test" ]; then
            echo "$test is not a valid file."
            return -1
        fi

        echo -en "\n"
        python $(dirname $0)/char_counter.py "$test" \
            || echo -e "\nSomething went wrong... Please send the entire error message above and the .tex file to Oskari... :)"
    else
        echo "Python not installed, please let Oskari know so he can try do something about it."
        return -1
    fi
}

main "$1"
ret_code=$?
echo -e "\nThis terminal window can be closed quickly with CMD-D."
read
exit $ret_code
