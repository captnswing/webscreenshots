#-*- coding: utf-8 -*-
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# http://guide.python-distribute.org
# http://packages.python.org/distribute/setuptools.html
setup(
    # provide basic metadata
    name="webscreenshots",
    version=0.8,
    author=u'Frank Hoffsümmer',
    description='take regular screenshots of websites',
    author_email='frank.hoffsummer@gmail.com',
    url='https://bitbucket.org/captnswing/webscreenshots',
    # install packages, see http://docs.python.org/distutils/setupscript.html#listing-whole-packages
    package_dir={'': 'src'},
    packages=find_packages('src'),
    # include all non-python files under source control, e.g. media/ and templates/ directories
    include_package_data=True,
    # make setuptools work with mercurial, see http://pypi.python.org/pypi/setuptools_hg
    setup_requires=["distribute", "setuptools_hg"],
    install_requires=[
        'distribute',
        'django',
        'PIL',
        'boto',
        'psycopg2',
        'celery-with-redis',
        'python-dateutil < 2',
        'flower',
        'ipython',
        'supervisor',
    ],
)
