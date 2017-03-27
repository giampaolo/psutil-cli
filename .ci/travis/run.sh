#!/bin/bash

set -e
set -x

PYVER=`python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))'`

# setup OSX
if [[ "$(uname -s)" == 'Darwin' ]]; then
    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi
    pyenv activate psutilcli
fi

# install psutilcli
python setup.py build
python setup.py develop

# run tests (with coverage)
if [[ "$(uname -s)" != 'Darwin' ]]; then
    coverage run psutilcli/test/runner.py --include="psutil-cli/*" --omit="test/*,*setup*"
else
    python psutil-cli/tests/runner.py
fi

if [ "$PYVER" == "2.7" ] || [ "$PYVER" == "3.5" ]; then
    # run linter (on Linux only)
    if [[ "$(uname -s)" != 'Darwin' ]]; then
        python -m flake8
    fi
fi
