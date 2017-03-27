#!/bin/bash

set -e
set -x

uname -a
python -c "import sys; print(sys.version)"

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    case "${PYVER}" in
        # py26)
        #     pyenv install 2.6.9
        #     pyenv virtualenv 2.6.9 psutilcli
        #     ;;
        py27)
            pyenv install 2.7.10
            pyenv virtualenv 2.7.10 psutilcli
            ;;
        # py32)
        #     pyenv install 3.2.6
        #     pyenv virtualenv 3.2.6 psutilcli
        #     ;;
        # py33)
        #     pyenv install 3.3.6
        #     pyenv virtualenv 3.3.6 psutilcli
        #     ;;
        py34)
            pyenv install 3.4.3
            pyenv virtualenv 3.4.3 psutilcli
            ;;
    esac
    pyenv rehash
    pyenv activate psutilcli
fi

if [[ $TRAVIS_PYTHON_VERSION == '2.6' ]] || [[ $PYVER == 'py26' ]]; then
    pip install -U ipaddress unittest2 argparse mock==1.0.1
elif [[ $TRAVIS_PYTHON_VERSION == '2.7' ]] || [[ $PYVER == 'py27' ]]; then
    pip install -U ipaddress mock
elif [[ $TRAVIS_PYTHON_VERSION == '3.2' ]] || [[ $PYVER == 'py32' ]]; then
    pip install -U ipaddress mock
elif [[ $TRAVIS_PYTHON_VERSION == '3.3' ]] || [[ $PYVER == 'py33' ]]; then
    pip install -U ipaddress
fi

pip install -U coverage coveralls flake8 pep8 setuptools
