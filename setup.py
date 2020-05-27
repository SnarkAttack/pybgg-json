import sys
import setuptools
from setuptools.command.test import test as TestCommand
    
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)
        
with open("README.md", "r") as fh:
    long_description = fh.read()
    
requirements = [
    'requests',
]

test_requirements = [
    'pytest',
]

setuptools.setup(
    name="pybgg-json",
    version="0.0.4",
    author="Patrick McQuay",
    author_email="patrick.mcquay@gmail.com",
    description="Python package to wrap BoardGameGeek XML API2 calls and produce JSON results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SnarkAttack/pybgg-json",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    test_suite='tests',
    tests_require=test_requirements,
    cmdclass = {'test': PyTest}
)
