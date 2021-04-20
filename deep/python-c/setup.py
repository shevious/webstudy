# setup.py

from distutils.core import setup, Extension

setup(name = "mylib",
        version = "1.0",
        description = "print log",
        author = "Samsjang",
        author_email = "samsjang@cdnetworks.co.kr",
        url = "http://www.cdnetworks.co.kr",
        ext_modules = [Extension("mylib", ["mylib.c"])]
        )
