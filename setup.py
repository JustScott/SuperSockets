from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()

VERSION = '0.0.3'
DESCRIPTION = "Easy to use implementation of the built in 'socket' library"

# Setting up
setup(
    name="supersockets",
    version=VERSION,
    license="MIT",
    author="JustScott",
    author_email="<justscottmail@protonmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url = "https://github.com/JustScott/SuperSockets",
    project_urls={
        "Bug Reports":"https://github.com/JustScott/SuperSockets/issues",
    },
    package_dir={"":"src"},
    packages=["supersockets"],
    install_requires=['listcrypt','rapidrsa'],
    keywords=['python','networking','sockets'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Networking',
    ]
)

