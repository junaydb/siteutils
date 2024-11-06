from setuptools import setup, find_packages

setup(
    name="siteutils",
    version="0.1.0",
    package_dir={"": "src"},
    py_modules=["siteutils"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "siteutils = siteutils:siteutils",
        ],
    },
)
