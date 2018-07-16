from io import open

from setuptools import find_packages, setup

with open("lunar/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(" '\"")
            break
    else:
        version = "0.0.1"

with open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

REQUIRES = []

setup(
    name="lunar",
    version=version,
    description="",
    long_description=readme,
    author="Eric Wang",
    author_email="wrqatw@gmail.com",
    maintainer="Eric Wang",
    maintainer_email="wrqatw@gmail.com",
    url="https://github.com/lroolle/lunar",
    license="MIT/Apache-2.0",
    keywords=[""],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=REQUIRES,
    tests_require=["coverage", "pytest"],
    packages=find_packages(),
)
