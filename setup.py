try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Dicio',
    version='v1.0.0',
    author='Felipe Pontes',
    author_email='felipemfpontes@gmail.com',
    packages=['dicio', 'tests'],
    test_suite='tests',
    url='https//github.com/felipemfp/dicio',
    license='MIT License',
    description='Unofficial Python API for Dicio.',
    long_description='Unofficial Python API for Dicio. \
        Usage: https://github.com/felipemfp/dicio.'
)
