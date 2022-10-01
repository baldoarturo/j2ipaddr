
import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="j2ipaddr",
    version="0.1.0",
    author="Arturo Baldo",
    author_email="baldoarturo@gmail.com",
    packages=["src"],
    description="Jinja2 filters for IP addresses, the easy way",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/baldoarturo/j2ipaddr",
    license='GNU GPL 3',
    python_requires='>=3.8',
    install_requires=['netaddr']
)