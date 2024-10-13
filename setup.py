from setuptools import setup, find_packages

setup(
    name="website_utils",
    version="0.1.0",
    package_dir={"": "src"},
    py_modules=["website_utils"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "website-utils = website_utils:website_utils",
        ],
    },
)
