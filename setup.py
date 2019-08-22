import setuptools

setuptools.setup(
    name='wandb_summary',
    version='0.1',
    description='A tiny CSV export micro-library for Weights and Biases.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Sam Pottinger',
    author_email='sam@datadrivenempathy.com',
    license='MIT',
    packages=['wandb_summary'],
    install_requires=[
      'wandb',
    ],
    entry_points = {
        'console_scripts': ['wandb-summary-export=wandb_summary.export:main'],
    }
)
