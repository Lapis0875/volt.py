from setuptools import setup, find_packages

with open('README.md', 'rt', encoding='utf-8') as f:
    long_desc = f.read()

# Setup module
setup(
    # Module name
    name="volt",
    # Module version
    version="0.1.0",
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
    url="https://github.com/Lapis0875/dpy_buttons",
    # Include module directory 'embed_tools'
    packages=find_packages(),
    # Dependencies : This project depends on module 'discord.py'
    install_requires=[],
    # Module`s python requirement
    python_requires=">=3.7",
    # Keywords about the module
    keywords=["discord api", "discord.py", "discord api wrapper"],
    # Tags about the module
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)