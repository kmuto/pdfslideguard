# python setup.py sdist bdist_wheel
from setuptools import setup, find_packages

setup(
    name='pdfslideguard',
    version='0.0.1', # リリースごとに更新
    author='Kenshi Muto',
    description='A tool to convert PDFs into high-resolution, searchable image-based PDFs to improve compatibility.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kmuto/pdfslideguard',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF>=1.25.4',
        'pypdf>=5.4.0',
        'reportlab>=4.3.1',
    ],
    entry_points={
        'console_scripts': [
            'pdfslideguard = pdfslideguard.pdfslideguard:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Topic :: Multimedia :: Graphics',
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
