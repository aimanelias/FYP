from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

AUTHOR_NAME = 'MUHAMMAD AIMAN'
SRC_REPO = 'src'  # package folder
LIST_OF_REQUIREMENTS = ['streamlit']  # also can use flask

setup(
    name=SRC_REPO,
    version='0.0.1',
    author=AUTHOR_NAME,
    author_email='aiman.elias67@gmail.com',
    description='A simple package for laptop recommender system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url='<github link>',  # Uncomment and add your GitHub link
    packages=[SRC_REPO],
    python_requires='>=3.7',
    install_requires=LIST_OF_REQUIREMENTS,
)
