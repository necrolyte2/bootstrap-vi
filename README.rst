.. image:: https://travis-ci.org/necrolyte2/bootstrap_vi.svg
    :target: https://travis-ci.org/necrolyte2/bootstrap_vi

.. image:: https://coveralls.io/repos/necrolyte2/bootstrap_vi/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/necrolyte2/bootstrap_vi?branch=master


============
bootstrap_vi
============

Bootstrap Virtualenv on system without pip or easy_install

It isn't terribly hard to get virtualenv installed, but often times it would be
much easier to be able to put in installation instructions a simple one line
curl to get a virtualenv setup and running.

Eventually it would be great to setup this project such that it could also be used
as a setuptools setup.py extension.

Bootstrapping a virtualenv
==========================

The idea is to be as simple as possible on a single line you can include in your
installation instructions

.. code-block:: bash

    wget https://raw.githubusercontent.com/necrolyte2/bootstrap_vi/master/bootstrap_vi.py -O- | python -

This would setup a virtualenv in the current directory under the venv directory.
You can supply any of the virtualenv's arguments after the word python and they will
be passed on to the virtualenv call.

So say you want to change the virtualenv's directory and prompt

.. code-block:: bash

    wget https://raw.githubusercontent.com/necrolyte2/bootstrap_vi/master/bootstrap_vi.py -O- | python - envdir --prompt="(myenv)"

This would then create the virtualenv in the envdir directory and set the prompt
for the environment to ``(myenv)``

Bootstrapping using setuptools
==============================

You can now bootstrap virtualenv in your project even easier through setuptools.

You just have to include the following inside your ``setup.py``

.. code-block:: python

    setup_requires = [
        'bootstrap_vi'
    ]

Now you can simply put in your installation docs the following to easily bootstrap
virtualenv for your project

.. code-block:: bash

    python setup.py bootstrap_virtualenv

This will do exactly the same thing as if you just ran

.. code-block:: bash

    python bootstrap_vi.py


Similarily, you can pass any virtualenv arguments

.. code-block:: bash

    python setup.py bootstrap_virtualenv envdir --prompt="(myenv)"
