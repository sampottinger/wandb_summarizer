import setuptools

setuptools.setup(
    name='wandb_summarizer',
    version='0.1',
    description='A tiny CSV export micro-library for Weights and Biases.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='A. Samuel Pottinger',
    license='MIT',
    packages=['wandb_summarizer'],
    install_requires=[
      'wandb',
    ],
    entry_points = {
        'console_scripts': ['wandb-summarizer-to-csv=wandb_summarizer.export:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    download_url='https://github.com/sampottinger/wandb_summarizer/archive/master.zip'
)
