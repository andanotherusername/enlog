from setuptools import setup, find_packages

setup(
    name="Enlog",
    version="0.1",
    author="Debdut Chakraborty",
    author_email="andanotheremailid@gmail.com",
    description="EndeavourOS Log Tool",
    long_description="Gathers selected system logs and generates a sharable link.",
    packages=["enlog", "enui"],
    entry_points={
        "console_scripts": [
            "enlog = enlog.main:main"
        ]
    }
)