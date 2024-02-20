import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ranking_aggregation",
    version="0.0.2",
    author="Noelia Rico,",
    author_email="noeliarico@uniovi.es",
    description="Ranking aggregation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.noeliarico.dev",
    project_urls={
        "Bug Tracker": "https://www.noeliarico.dev",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["numpy", "dotenv"],
)
