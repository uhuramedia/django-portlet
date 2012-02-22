import os
from setuptools import setup, find_packages

VERSION = "0.1"

setup(
    name="fm.portlet",
    version = VERSION,
    author="Julian Bez",
    author_email="julian@freshmilk.tv",
    url="https://github.com/Freshmilk/",
    description="""FM portlet system""",
    packages=find_packages(),
    namespace_packages = [],
    include_package_data = True,
    zip_safe=False,
    license="None",
    install_requires=[]
)
