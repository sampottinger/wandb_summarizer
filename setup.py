import setuptools

setuptools.setup(
    name='wandb_summarizer',
    version='0.1',
    description='A tiny CSV export micro-library for Weights and Biases.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Sam Pottinger',
    author_email='sam@datadrivenempathy.com',
    license='MIT',
    packages=['wandb_summarizer'],
    install_requires=[
      'wandb',
    ],
    entry_points = {
        'console_scripts': ['wandb-summarizer-export=wandb_summarizer.export:main'],
    }
)
