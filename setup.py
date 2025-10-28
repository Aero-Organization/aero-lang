# setup.py
from setuptools import setup, find_packages
import os

#
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

#
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), "aero", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    raise RuntimeError("Unable to find version string.")

setup(
    name="aero-lang",
    version=get_version(),
    author="codewithzaqar",
    author_email="hakobyanzaqar3@gmail.com",
    description="A fast, fluid language built for lightweight systems and high-speed execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Compilers",
        "Topic :: System :: Software Distribution",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "aero=aero.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
