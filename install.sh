#!/bin/bash

#########################################
# Installing python and necessary packages
# locally. This script will install python
# into the ~/$ROOT_TO_PYTHON/bin directory
# and install dotenv + telethon modules
#########################################

ROOT_TO_PYTHON='local/python'

# installing python 3.9.1
mkdir -p ~/$ROOT_TO_PYTHON
curl -fsSL https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz > Python-3.9.1.tgz
tar xvzf Python-3.9.1.tgz
cd Python-3.9.1
make clear
./configure
make
make altinstall prefix=~/$ROOT_TO_PYTHON # specify local installation directory
ln -s ~/$ROOT_TO_PYTHON/bin/python3.9 ~/$ROOT_TO_PYTHON/bin/python
cd ..

# # install setuptools and pip for package management
# wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e
# tar xvzf setuptools-0.6c11.tar.gz
# cd setuptools-0.6c11
# ~/$ROOT_TO_PYTHON/bin/python setup.py install  # specify the path to the python you installed above
# cd ..
# wget http://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz#md5=db8a6d8a4564d3dc7f337ebed67b1a85
# tar xvzf pip-1.2.1.tar.gz
# cd pip-1.2.1
# ~/$ROOT_TO_PYTHON/bin/python setup.py install  # specify the path to the python you installed above

rm -rf Python-3.9.1
rm -rf Python-3.9.1.tgz

# Now you can install other packages using pip
~/$ROOT_TO_PYTHON/bin/python -m pip install dotenv # TODO: THIS HAS TO WORK
~/$ROOT_TO_PYTHON/bin/python -m pip install telethon # TODO: THIS HAS TO WORK
