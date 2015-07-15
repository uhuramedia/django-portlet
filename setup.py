import os
from setuptools import setup, find_packages

VERSION = "0.4"

setup(
    name="django-portlet",
    version = VERSION,
    author="Nar Chhantyal",
    author_email="julian@freshmilk.tv",
    url="https://github.com/Freshmilk/",
    description="""Django portlet system""",
    packages=find_packages(),
    namespace_packages = [],
    include_package_data = True,
    package_data={
    'portlet': [
        'templates/portlet/*',
        ]
    },
    zip_safe=False,
    license="None",
    install_requires=['simplejson']
)
