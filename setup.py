import setuptools

# Long Description
with open('README.md', 'r') as file:
    long_description = file.read()

# Dependencies
with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setuptools.setup(
    name="Satella-lauslim12",
    version="1.0.0",
    author="Nicholas Dwiarto Wirasbawa",
    author_email="nicholasdwiarto@yahoo.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lauslim12/Satella",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-3-Clause",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
