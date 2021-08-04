from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = "0.0.1"

setup(
    name="stemaway",
    version=__version__,
    description="Replicating and extending research done by Percha and Altman 2015 on Learning the Structure of Biomedical Relationships from Unstructured Text”",
    url="",
    download_url="",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    author="Matthew Taruno",
    # install_requires=install_requires,
    setup_requires=[],
    # dependency_links=dependency_links,
    author_email="matthew.taruno@gmail.com",
)
