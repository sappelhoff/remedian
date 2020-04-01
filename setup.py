"""Setup remedian."""
from setuptools import setup, find_packages
import os
from os import path
import io

# get the version
version = None
with open(os.path.join("remedian", "__init__.py"), "r") as fid:
    for line in (line.strip() for line in fid):
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip("'")
            break
if version is None:
    raise RuntimeError("Could not determine version")

here = path.abspath(path.dirname(__file__))

# Get long description from README file
with io.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='remedian',
      version=version,
      description='Remedian: robust averaging of large data sets',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='http://github.com/sappelhoff/remedian',
      author='Stefan Appelhoff',
      author_email='stefan.appelhoff@mailbox.org',
      license='MIT',
      classifiers=[
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research'
      ],
      keywords='remedian median memory efficient big data',
      packages=find_packages(),
      install_requires=['numpy>=1.14.1'],
      python_requires='>=2.7',
      project_urls={
        "Documentation": "https://remedian.readthedocs.io/en/latest",
        'Bug Reports': 'https://github.com/sappelhoff/remedian/issues',
        'Source': 'https://github.com/sappelhoff/remedian'
      })
