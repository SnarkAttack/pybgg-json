import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybgg-json",
    version="0.0.1",
    author="Patrick McQuay",
    author_email="patrick.mcquay@gmail.com",
    description="Python package to wrap BoardGameGeek XML API2 calls and produce json results",
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
)