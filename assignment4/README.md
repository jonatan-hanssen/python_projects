# Assignment 4

This assignment implements a web scraper that finds interesting information from
wikipedia.

## Requirements

Requires the python packages ```requests```, ```beautifulsoup4```, ```matplotlib``` and ```pandas```.

To test the code, I recommend using a virtual environment. The following shell commands will install only the required packages and runs pytest, and should clear all 37 tests.

```
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
$ pytest tests/
```

To leave the virtual environment, simply type ```$ deactivate``` in your shell.

The scripts have been successfully run in the following environments (both with the virtual environment described above):

#### Personal laptop
```
$ uname -rs
Linux 6.0.1-arch2-1
$ python3 --version
Python 3.10.8
```
#### Ifi workstation
```
$ uname -rs
Linux 4.18.0-372.13.1.el8_6.x86_64
$ python3 --version
Python 3.9.12
```

