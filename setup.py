from setuptools import setup, find_packages

setup(
    name='infiray_show',
    version='0.1.0',
    author='Florin Tobler',
    author_email='florin.tobler@hotmail.com',
    description='A project for thermal imaging using InfiRay P2 pro camera',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'infiray-show=infiray_show.main:infiray_show',
        ],
    },
    install_requires=[
        'opencv-python',
        'numpy',
    ],
)