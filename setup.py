# from utility.library import *


# with open("README.md", "r") as f:
#     readme = f.read()

# setup(
#     name=SettingsProps.PIP_NAME,
#     version=SettingsProps.PIP_VERSION,
#     author=SettingsProps.SETUP_AUTHOR,
#     author_email=SettingsProps.SETUP_AUTHOR_EMAIL,
#     description=SettingsProps.SETUP_DESCRIPTION,
#     license=SettingsProps.SETUP_LICENSE,
#     long_description=readme,
#     long_description_content_type="text/markdown",
#     include_package_data=True,
#     url=SettingsProps.SETUP_URL,
#     # download_url=SettingsProps.SETUP_DOWNLOADABLE_URL,
#     packages=setuptools.find_packages(),
#     install_requires=["requests","pandas","websocket-client","rel"],
#     classifiers=[
#         "Programming Language :: Python :: 3.8",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#         "Natural Language :: English",
#         "Intended Audience :: Developers",
#     ],

#     python_requires='>=3.7',

#     project_urls={
#         "Documentation": SettingsProps.SETUP_APIDOCS,
#     },
# )


from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="Ant-A3-tradehub-sdk-production",
    version="1.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="Alice Blue TradeHub SDK",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pandas",
        "websocket-client",
        "rel",
        "pycryptodome"
    ],
    python_requires=">=3.7",
)