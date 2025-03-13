from setuptools import setup, find_packages

setup(
    name="icloud-versioning",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "icloud-versioning=icloud_versioning.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for managing iCloud file versioning",
    keywords="icloud, versioning, backup",
    python_requires=">=3.6",
)