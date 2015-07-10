=========
Changelog
=========

0.0.4
=====

- setup_requires only includes nose. Prior, it included all test requirements which
  in turn meant any project placing bootstrap_vi into its setup_requires would mean
  they would be downloaded as well
- Misc Readme clarifications

0.0.3
=====

- Fixed another bug when entry_point command was used to call script
- Fixed setup.py(hopefully) to be more correct with regards to py_module

0.0.2
=====

- Fixed bug when running with just python interpreter
- Added support for setuptools extension
