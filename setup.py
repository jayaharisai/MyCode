from setuptools import setup, find_packages

setup(
    name='MyCode',  # Name of your package
    version='1.1.0',
    packages=find_packages(),
    install_requires=[  # List of dependencies
        "boto3",
        "requests",
        "numpy", "polars",
        "faker", "tqdm"
    ],
    author='Jayaharisai',
    author_email='jayaharisai1212@gmail.com',
    description='A simple Python package that says "Hello, world!"',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jayaharisai/MyCode.git',  # Link to your GitHub project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Ensure this classifier matches your license
        'Operating System :: OS Independent',
    ],
    license='MIT',  # Correctly define the license directly here
)
