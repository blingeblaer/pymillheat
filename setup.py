import setuptools

def readme():
    with open("README.md") as f:
        README = f.read()
    return README

setuptools.setup(
    name="pymillheat",
    version="1.0.4",
    url="https://github.com/Erlendeikeland/pymillheat",
    author="Erlendeikeland",
    description="Library for interacting with millheat api",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.5.3",
    author_email="Erlend132@gmail.com",
    install_requires=["aiohttp", "async_timeout", "urllib3"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
)
