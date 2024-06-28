# Copyright 2024-present, Moverse
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
import re
import io
import logging

from setuptools import (
    setup,
    find_packages
)
from pkg_resources import (
    DistributionNotFound,
    get_distribution, 
    parse_version,
)

logger = logging.getLogger()
logging.basicConfig(format='%(levelname)s - %(message)s')

def get_readme():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()

def get_requirements():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(base_dir, "requirements.txt"), encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


PACKAGE_NAME = 'rerun-animation'
VERSION = '0.0.1'
AUTHOR = 'Moverse P.C.'
EMAIL = 'info@moverse.ai'
LICENSE = 'Apache 2.0'
URL = ''
CODE_URL = ''
DOCS_URL = ''
DESCRIPTION = ''
KEYWORDS = ''

if __name__ == '__main__':
    logger.info(f"Installing {PACKAGE_NAME} (v{VERSION}) ...")
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=EMAIL,
        description=DESCRIPTION,
        long_description=get_readme(),
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        licence_file='LICENSE',
        url=URL,
        project_urls={
            'Documentation': DOCS_URL,
            'Source': CODE_URL,
        },
        packages=find_packages(exclude=('docs', 'data', 'build', 'dist', 'scripts')),
        install_requires=get_requirements(),
        include_package_data=True,
        python_requires='~=3.10',
        package_dir={'rerun_animation': 'rerun_animation'},
        package_data={'rerun_animation': ['configs/**/*.ini']},
        entry_points={
            'console_scripts': [
                'rerun-animation=rerun_animation.actions.app:run',
                'rerun-animation-deploy=rerun_animation.actions.deploy:run',
                'rerun-animation-stream=rerun_animation.actions.stream:run',
                'rerun-animation-config=rerun_animation.actions.config:run',
            ],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
            "Topic :: Scientific/Engineering :: Visualization",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],    
    )