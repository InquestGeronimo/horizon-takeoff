from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

NAME = "cloud-takeoff"
VERSION = "0.0.1"
AUTHOR = "InquestGeronimo"
EMAIL = "rcostanl@gmail.com"
LD_CONTENT_TYPE = "text/markdown"
DESCRIPTION = "LLM deployment on AWS with the Takeoff Server"
LONG_DESCRIPTION = "n/a."
PACKAGE_DIR = {"": "src"}
PACKAGES = find_packages("src")
ENTRY_POINTS={"console_scripts": ["takeoff = src.takeoff.startup"]},
DEPENDENCIES = ["boto3>=1.34.4", "pyyaml>=6.0.1", "rich>=12.6.0"]
KEYWORDS = ["cloud", "titanml", "server", "LLM", "NLP", "MLOps", "deployment"]
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: Unix",
]

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description_content_type=LD_CONTENT_TYPE,
    long_description=LONG_DESCRIPTION,
    package_dir=PACKAGE_DIR,
    packages=PACKAGES,
    install_requires=DEPENDENCIES,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS
)