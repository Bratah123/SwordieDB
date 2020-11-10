from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='swordiedb',
    version='0.0.4',
    description='A database API for swordie-ms based maplestory sources',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Brandon Nguyen',
    author_email='brandonnguyen3301@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='database, swordie',
    packages=find_packages(),
    install_requires=['mysql-connector-python-rf']
)
