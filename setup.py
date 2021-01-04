import sys
if sys.version_info < (2, 7, 0):
    print('You need Python 2.7 or better to install calweek')
    sys.exit(1)


from setuptools import setup

setup(
    name = 'calweek',
    version = '0.4.0',
    description = 'Objects representing a (non-ISO) week',
    author='Ray Burr',
    author_email='ryb@nightmare.com',
    url='http://github.com/wonkyweirdy/calweek',
    py_modules=['calweek'],
    license='BSD',
    long_description=open("README.rst").read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
