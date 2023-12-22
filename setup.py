from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

NAME = "horizon"
VERSION = "0.0.177"
AUTHOR = "InquestGeronimo"
EMAIL = "rcostanl@gmail.com"
LD_CONTENT_TYPE = "text/markdown"
DESCRIPTION = "Auto-deploy the Takeoff Server on AWS for LLM inference"
LONG_DESCRIPTION = "n/a."
PACKAGE_DIR = {"": "src"}
PACKAGES = find_packages("src")
PACKAGE_DATA = {'src.horizon': ['scripts/*']}
ENTRY_POINTS = {"console_scripts": ["horizon=horizon.takeoff:main"]}
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
    package_data=PACKAGE_DATA,
    entry_points=ENTRY_POINTS,
    include_package_data=True,
    install_requires=DEPENDENCIES,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS
)