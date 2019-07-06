import pathlib

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='Dicio',
    version='1.2.0',
    author='Felipe Pontes',
    author_email='felipemfpontes@gmail.com',
    packages=['dicio'],
    test_suite='tests',
    url='https://github.com/felipemfp/dicio',
    license='MIT License',
    description='Unofficial Python API for Dicio.',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Utilities',
    ],
)
