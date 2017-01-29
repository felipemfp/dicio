try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Dicio',
    version='v1.0.1',
    author='Felipe Pontes',
    author_email='felipemfpontes@gmail.com',
    packages=['dicio', 'tests'],
    test_suite='tests',
    url='https://github.com/felipemfp/dicio',
    license='MIT License',
    description='Unofficial Python API for Dicio.',
    long_description='Unofficial Python API for Dicio. \
        Usage: https://github.com/felipemfp/dicio.',
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
