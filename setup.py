"""Setup remedian."""
from setuptools import setup, find_packages
from os import path
import io

here = path.abspath(path.dirname(__file__))

# Get long description from README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='remedian',
      version='0.1.0',
      description='Remedian: robust averaging of large data sets',
      long_description=long_description,
      long_description_content_type='text/markdown',
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
      extras_require={
        'test': ['nose>=1.3.7']
      },
      project_urls={
        'Bug Reports': 'https://github.com/sappelhoff/remedian/issues',
        'Source': 'https://github.com/sappelhoff/remedian'
      })
