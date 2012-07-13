#!/usr/bin/env python
from distutils.core import setup
setup(
    name = "django_qspickle",
    version = "0.1",
    packages = ['qspickle', ],
    author='CBWhiz',
    author_email='CBWhiz@gmail.com',
    description='Django queryset query pickling',
    long_description='Allows you to pickle a QuerySet (the query), not the results of executing the query.',
    keywords = "django queryset pickle",
    url = "https://github.com/CBWhiz/django_qspickle",
    license = "GNU General Public License (GPL)",
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)