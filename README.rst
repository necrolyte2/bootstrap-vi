.. image:: https://badge.fury.io/py/bootstrap_vi.svg
    :target: http://badge.fury.io/py/bootstrap_vi

.. image:: https://img.shields.io/pypi/dm/bootstrap_vi.svg
    :target: https://pypi.python.org/pypi/bootstrap_vi

.. image:: https://travis-ci.org/necrolyte2/bootstrap_vi.svg
    :target: https://travis-ci.org/necrolyte2/bootstrap_vi

.. image:: https://coveralls.io/repos/necrolyte2/bootstrap_vi/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/necrolyte2/bootstrap_vi?branch=master


============
bootstrap_vi
============

Bootstrap Virtualenv on system without pip or easy_install

It isn't terribly hard to get virtualenv installed, but often times it would be
much easier to be able to just use a single quick command to get a virtualenv up and
running.

Also, putting the instructions on how to setup a virtualenv in installation 
instructions is a bit redundant and not concise enough for novice python users.

This project allows you to very easily use a single command to bootstrap a
virtualenv to solve these issues.

Bootstrapping a virtualenv
==========================

The idea is to be as simple as possible on a single line you can include in your
installation instructions

.. code-block:: bash

    $> wget https://raw.githubusercontent.com/necrolyte2/bootstrap_vi/master/bootstrap_vi.py -O- | python -

This would setup a virtualenv in the current directory under the venv directory.
You can supply any of the virtualenv's arguments after the word python and they will
be passed on to the virtualenv call.

If you want to change the virtualenv's directory and prompt for example:

.. code-block:: bash

    $> wget https://raw.githubusercontent.com/necrolyte2/bootstrap_vi/master/bootstrap_vi.py -O- | python - envdir --prompt="(myenv)"

This would then create the virtualenv in the envdir directory and set the prompt
for the environment to ``(myenv)$PS1``

Bootstrapping using setuptools
==============================

You can also bootstrap virtualenv in a python project by leveraging setup.py.

You just have to include the following inside your ``setup.py``

.. code-block:: python

    setup_requires = [
        'bootstrap_vi'
    ]

Now you can simply put in your installation docs the following to easily bootstrap
virtualenv for your project.

This would be very similar to the first wget call above.

.. code-block:: bash

    $> python setup.py bootstrap_virtualenv


Similarity to the second wget example above, you can pass any virtualenv arguments

.. code-block:: bash

    $> python setup.py bootstrap_virtualenv envdir --prompt="(myenv)"

This would also create a virtualenv in the envdir directory and set the prompt to
``(myenv)$PS1``
