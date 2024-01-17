from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name="rag",
    version="1.0.6",
    packages=find_packages(),
    author="",
    author_email="",
    description="The RAGtriever chatbot",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=requirements,
    extras_require={"dev": ["pytest", "wheel", "twine", "black", "setuptools"]}
)