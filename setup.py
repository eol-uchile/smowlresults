"""Setup for iframe XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='smowlresults-id-xblock',
    version='78.4',
    description='SMOWL RESULTS',
    packages=[
        'smowlresults',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'smowlresults = smowlresults:IframeWithAnonymousIDXBlock',
        ],
        "lms.djangoapp": [
            "smowlresults = smowlresults.apps:SmowlResultsConfig",
        ],
        "cms.djangoapp": [
            "smowlresults = smowlresults.apps:SmowlResultsConfig",
        ]
    },
    package_data=package_data(
        "smowlresults", ["static", "templates", "public"]),
)
