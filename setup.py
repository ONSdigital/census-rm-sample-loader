from pathlib import Path

import setuptools

setuptools.setup(
    name="census_rm_sample_loader",
    version="0.0.1",
    description="Scripts to load samples",
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/ONSdigital/census-rm-sample_loader",
    packages=setuptools.find_packages(),
)
