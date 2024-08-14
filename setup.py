from setuptools import setup, find_packages

setup(
    name="diffeo_toolkit",
    version="0.0",
    author="Clark Miyamoto, Alex Jiang",
    description="Toolkit for diffeomorphisms research",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/clarkmiyamoto/diffeo_toolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    tests_require=[
        "pytest",
    ],
)

