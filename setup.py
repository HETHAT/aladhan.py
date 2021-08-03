import os
import re

from setuptools import setup


def get_version(package):
    """Return package version as listed in `__version__`
    in `init.py`."""
    path = os.path.join(package, "__init__.py")
    version = ""
    with open(path, "r", encoding="utf8") as init_py:
        version = re.search(
            r"^__version__\s*=\s*['\"]([^'\"]*)['\"]",
            init_py.read(),
            re.MULTILINE,
        ).group(1)

    if not version:
        raise RuntimeError(f"__version__ is not set in {path}")

    return version


def get_packages(package):
    """Return root package and all sub-packages."""
    return [
        dirpath
        for dirpath, *_ in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


def get_long_description(filename: str = "README.rst"):
    """Return the README."""
    with open(filename, "r", encoding="utf8") as readme:
        long_description = readme.read()
    return long_description


def get_requirements(filename: str = "requirements.txt"):
    """Return the requirements."""
    requirements = []
    with open(filename, "r", encoding="utf8") as requirements_txt:
        requirements = requirements_txt.read().splitlines()
    return requirements


extras_require = {
    "async": get_requirements("reqs/async-requirements.txt"),
    "sync": get_requirements("reqs/sync-requirements.txt"),
}

setup(
    name="aladhan.py",
    version=get_version("aladhan"),
    url="https://github.com/HETHAT/aladhan.py",
    license="MIT",
    description="A Python wrapper for the Aladhan prayer times API",
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    author="HETHAT",
    author_email="zhethat@gmail.com",
    packages=get_packages("aladhan"),
    python_requires=">=3.6",
    install_requires=get_requirements(),
    extras_require=extras_require,
    project_urls={
        # "Documentation": "",
        "Issue tracker": "https://github.com/HETHAT/aladhan.py/issues"
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
