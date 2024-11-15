from setuptools import setup, find_packages

setup(
    name='Gomoku',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'gomoku=main:lanch_game',
        ],
    },
    author='Mohamed alaoui',
    author_email='malaoui@student.1337.ma',
    description='Gomuku Project',
    url='https://github.com/sboof911/Gomoku',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)