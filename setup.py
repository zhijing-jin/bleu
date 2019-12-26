from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='bleu',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    package_dir={'mypkg': 'bleu'},
    # package_data={'mypkg': ['data/*.json']},
    license='BSD 3-Clause',
    description='A Python Wrapper to calculate standard BLEU scores for NLP',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['efficiency'],
    url='https://github.com/zhijing-jin/bleu',
    author='Zhijing Jin',
    author_email='zhijing.jin@connect.hku.hk'
)
