import setuptools

setuptools.setup(
    name="persephone",
    version="1.0",
    packages=["persephone"],
    scripts=["bin/persephone"],
    author="ememilyly",
    url="https://github.com/ememilyly/persephone",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'discord.py==2.3.1',
        'ffxivweather',
        'Google-Images-Search',
    ]
)
