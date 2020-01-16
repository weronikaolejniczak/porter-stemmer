import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='porterstemmer',
    version='0.1',
    packages=[''],
    package_dir={'': 'porter stemmer'},
    url='https://github.com/weronikaolejniczak/porterstemmer',
    license='MIT',
    author='Weronika',
    author_email='wer.olejniczak@gmail.com',
    description='Natural Language Processing project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
