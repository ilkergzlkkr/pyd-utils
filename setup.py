import re, setuptools

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = ""
with open("pyutils/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

extras_require = {"dev": ["black", "pytest", "pytest-asyncio", "flake8"]}


setuptools.setup(
    name="pyd-utils",
    version=version,
    description="pyd-utils",
    author="ilkergzlkkr",
    author_email="guzelkokarilker@gmail.com",
    packages=["pyutils"],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
)
