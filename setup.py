from setuptools import (
    setup,
    find_packages
)


with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='simple_flask_restful',
    version='0.3.0',
    author='William Wang',
    author_email='williamwangatsydney@gmail.com',
    description='wrap up flask for restful interface',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AutomationLover/simple_flask_restful',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements
)
