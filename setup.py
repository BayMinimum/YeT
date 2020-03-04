from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

github_url = 'https://github.com/BayMinimum/YeT'

setup(
    name='YeT',
    version='0.1.0',
    description='Elegant TeX script in YAML style',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=github_url,
    author='Sangbum Kim',
    author_email='bearksb1115@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='latex yaml',

    py_modules=["yet"],
    python_requires='>=3.6',
    install_requires=['PyYAML'],

    entry_points={
        'console_scripts': [
            'yet=yet:main',
        ],
    },

    project_urls={
        'Bug Reports': github_url + '/issues',
        'Source': github_url,
    },
)
