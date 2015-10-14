#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sockjs-tornado==1.0.0',
    'tornado==3.2.2',
    'argparse',

    # simplejson is really required for py3 support to avoid encoding problems
    'simplejson'
]

setup(
    name='thunderpush',
    version='1.0.0',
    author='Krzysztof Jagiello',
    author_email='me@kjagiello.com',
    description='Tornado and SockJS based, complete Web push solution.',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    license='BSD',
    include_package_data=True,
    url='https://github.com/thunderpush/thunderpush',
    test_suite='thunderpush.tests.suite',
    entry_points={
        'console_scripts': [
            'thunderpush = thunderpush.runner:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
)
