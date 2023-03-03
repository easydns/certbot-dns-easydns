from setuptools import setup
from setuptools import find_packages
import re

VERSIONFILE = "certbot_dns_easydns/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {VERSIONFILE}")
with open("README.rst", "r") as fh:
    long_description = fh.read()


install_requires = [
    "acme>=0.29.0",
    "certbot>=0.34.0",
    "setuptools",
    "dns-lexicon",
]

docs_extras = [
    "sphinx",
    "sphinx-rtd-theme",
]

test_extras = [
    "pytest",
]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst")) as f:
    long_description = f.read()

setup(
    name="certbot-dns-easydns",
    version=version,
    description="EasyDNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/easydns/certbot-dns-easydns",
    author="Caleb S. Cullen",
    author_email="certbot-dev@easydns.com",
    license="Apache License 2.0",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        "docs": docs_extras,
        "test": test_extras,
    },
    entry_points={
        "certbot.plugins": [
            "dns-easydns = certbot_dns_easydns.dns_easydns:Authenticator"
        ]
    },
    test_suite="certbot_dns_easydns",
)
