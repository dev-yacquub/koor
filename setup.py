from setuptools import setup, find_packages

setup(
    name="soomaalipy",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "koor=koor.cli:main",
            "somali=soomaalipy.cli:main",
            "sompy=soomaalipy.cli:main",
        ],
    },
)
