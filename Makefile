# Shortcuts for various tasks (UNIX only).
# To use a specific Python version run: "make install PYTHON=python3.3"
# You can set the variables below from the command line.

PYTHON = python
TSCRIPT = psutilcli/test/runner.py
ARGS =

# List of nice-to-have dev libs.
DEPS =

# In not in a virtualenv, add --user options for install commands.
INSTALL_OPTS = `$(PYTHON) -c "import sys; print('' if hasattr(sys, 'real_prefix') else '--user')"`


all: test

# ===================================================================
# Install
# ===================================================================

# Remove all build files.
clean:
	rm -rf `find . -type d -name __pycache__ \
		-o -type f -name \*.bak \
		-o -type f -name \*.orig \
		-o -type f -name \*.pyc \
		-o -type f -name \*.pyd \
		-o -type f -name \*.pyo \
		-o -type f -name \*.rej \
		-o -type f -name \*.so \
		-o -type f -name \*.~ \
		-o -type f -name \*\$testfn`
	rm -rf \
		*.core \
		*.egg-info \
		*\$testfile* \
		.coverage \
		.tox \
		build/ \
		dist/ \
		docs/_build/ \
		htmlcov/ \
		tmp/

_:


# Compile without installing.
build: _
	$(PYTHON) setup.py build
	rm -rf tmp

# Install this package + GIT hooks. Install is done:
# - as the current user, in order to avoid permission issues
# - in development / edit mode, so that source can be modified on the fly
install: build
	# make sure setuptools is installed (needed for 'develop' / edit mode)
	$(PYTHON) -c "import setuptools"
	$(PYTHON) setup.py develop $(INSTALL_OPTS)
	rm -rf tmp

# Uninstall this package via pip.
uninstall:
	cd ..; $(PYTHON) -m pip uninstall -y -v psutil-cli

# Install PIP (only if necessary).
install-pip:
	$(PYTHON) -c \
		"import sys, ssl, os, pkgutil, tempfile, atexit; \
		sys.exit(0) if pkgutil.find_loader('pip') else None; \
		pyexc = 'from urllib.request import urlopen' if sys.version_info[0] == 3 else 'from urllib2 import urlopen'; \
		exec(pyexc); \
		ctx = ssl._create_unverified_context() if hasattr(ssl, '_create_unverified_context') else None; \
		kw = dict(context=ctx) if ctx else {}; \
		req = urlopen('https://bootstrap.pypa.io/get-pip.py', **kw); \
		data = req.read(); \
		f = tempfile.NamedTemporaryFile(suffix='.py'); \
		atexit.register(f.close); \
		f.write(data); \
		f.flush(); \
		print('downloaded %s' % f.name); \
		code = os.system('%s %s --user' % (sys.executable, f.name)); \
		f.close(); \
		sys.exit(code);"

# ===================================================================
# Tests
# ===================================================================

# Run all tests.
test: install
	$(PYTHON) $(TSCRIPT)

# ===================================================================
# Linters
# ===================================================================

pep8:
	@git ls-files | grep \\.py$ | xargs $(PYTHON) -m pep8

pyflakes:
	@export PYFLAKES_NODOCTEST=1 && \
		git ls-files | grep \\.py$ | xargs $(PYTHON) -m pyflakes

flake8:
	@git ls-files | grep \\.py$ | xargs $(PYTHON) -m flake8

# ===================================================================
# GIT
# ===================================================================

# Install GIT pre-commit hook.
install-git-hooks:
	ln -sf ../../.git-pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
