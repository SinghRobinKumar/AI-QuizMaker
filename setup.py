from setuptools import setup, find_packages

setup(
    name="MCQ-Gen",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain_community",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    author="Robin",
    author_email="singhrobinkumar0@gmail.com",
    python_requires='>=3.6',
)