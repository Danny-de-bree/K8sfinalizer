import setuptools

setuptools.setup(
    name="k8sfinalizer",
    version="0.0.1",
    author="Danny de Bree",
    description="A package to clean up terminating namespaces",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['kubernetes'],
    entry_points={
        'console_scripts': [
            'k8sfinalizer = k8sfinalizer.main:main'
        ]
    }
)