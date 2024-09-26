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
    project_urls={
        "Source Code": "https://github.com/djoroya/runstep",
        "Bug Tracker": "https://github.com/djoroya/runstep/issues",
    },
    # from requeriments.txt
    install_requires=[
        "loadsavejson @ git+https://github.com/djoroya/loadjson.git",
        "colorama"
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
