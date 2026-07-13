import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appgoblin-itunes-scraper",
    version="0.9.7",
    author="James O'Claire",
    author_email="james@appgoblin.info",
    description="A lightweight iTunes App Store scraper hard forked from the Digital Methods Initiative project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/appgoblin-dev/appgoblin-itunes-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    install_requires=["requests"],
)
