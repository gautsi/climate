import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="climate",
    version="0.0.1",
    author="Gautam Sisodia",
    packages=setuptools.find_packages(),
    classifiers=["Progamming Language :: Python :: 3"],
    dependency_links=['http://github.com/gautsi/pygsutils/tarball/master#egg=pygsutils-0.0.1']
)
