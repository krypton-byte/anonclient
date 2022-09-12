
from setuptools import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))

setup(
  name = 'anonclient', 
  long_description=open(base_dir+'/README.md','r').read(),
  long_description_content_type='text/markdown',
  packages = ['anonclient'],
  include_package_data=True,
  version = '0.1.6',
  license='MIT',
  description = 'ANONCHAT API',
  author = 'Krypton Byte',
  author_email = 'galaxyvplus6434@gmail.com',
  url = 'https://github.com/krypton-byte/anonclient',
  download_url = 'https://github.com/krypton-byte/anonclient/archive/0.1.6.tar.gz',
  keywords = ['anonchat', 'client', 'api', 'fullduplex'],
  install_requires=[           
        'protobuf',
        'websockets',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)