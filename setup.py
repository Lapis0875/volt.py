from setuptools import setup, find_packages

with open('README.md', 'rt', encoding='utf-8') as f:
    long_desc = f.read()

with open('requirements.txt', 'rt', encoding='utf-8') as f:
    requirements = f.readlines()

with __import__('volt.__init__.py') as module_info:
    version = module_info.__version__

extra_requires = {
    'voice': [],
    'speed': ['uvloop']
}

packages = [
    'volt',
    'volt.types',
    'volt.utils',
    'volt.ext.extensions',
    'volt.ext.ocm',
]

# Setup module
setup(
    # Module name
    name="volt.py",
    # Module version
    version="0.0.1",
    # License - MIT!
    license='MIT',
    # Author (Github username)
    author="Lapis0875",
    # Author`s email.
    author_email="lapis0875@kakao.com",
    # Short description
    description="Wrapper of discord api for discord.py. Personal project for my study.",
    # Long description in REAMDME.md
    long_description_content_type='text/markdown',
    long_description=long_desc,
    # Project url
    url="https://github.com/Lapis0875/volt.py",
    project_urls={
        "Documentation": "https://lapis0875.gitbook.io/volt-api-docs/",
        "Issue tracker": "https://github.com/Lapis0875/volt.py/issues",
        'Donate': 'https://www.patreon.com/lapis0875'
    },
    # Include module directory 'embed_tools'
    packages=packages,
    # Dependencies : This project depends on module 'discord.py'
    install_requires=requirements,
    extra_requires=extra_requires,
    # Module`s python requirement
    python_requires=">=3.7.0",
    # Keywords about the module
    keywords=["discord api", "discord.py", "discord api wrapper"],
    # Tags about the module
    classifiers=[
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)