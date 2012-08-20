#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sockjs-tornado==0.0.4',
    'tornado==2.3',
    'wsgiref==0.1.2',
]

setup(
    name='thunderpush',
    version='0.9.4',
    author='Krzysztof Jagiello',
    author_email='balonyo@gmail.com',
    description='Tornado and SockJS based, complete Web push solution.',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    license='BSD',
    include_package_data=True,
    url='https://github.com/kjagiello/thunderpush',
    test_suite='thunderpush.testsuite.suite',
    entry_points={
        'console_scripts': [
            'thunderpush = thunderpush.runner:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
)