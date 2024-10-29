from setuptools import setup, find_packages

setup(
    name="runstep",
    version="0.1.0",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Deyviss Jesús Oroya Villalta",
    author_email="djoroya@gmail.com",
    url="https://github.com/djoroya/runstep",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "runstep_gui = runstep.app:main",
            "mkdirsimln = runstep.mkdirsimln:main",
        ],
    },
    project_urls={
        "Source Code": "https://github.com/djoroya/runstep",
        "Bug Tracker": "https://github.com/djoroya/runstep/issues",
    },
    # from requeriments.txt
    install_requires=[ # Dependencias necesarias para instalar tu paquete
        open('requirements.txt').read().splitlines()
    ],
    python_requires='>=3.6',  # Versión mínima de Python requerida
    classifiers=[  # Clasificadores que ayudan a otros desarrolladores a encontrar tu proyecto
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Tipo de licencia
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        "runstep": ["runstep/bin/*"],
    },
)
