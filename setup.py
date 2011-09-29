import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = "c2cgeoportal, generic gis protail made by camptocamp"

requires = [
    'pyramid',
    'WebError',
    'psycopg2',
    'sqlalchemy',
    'sqlalchemy-migrate',
    'sqlahelper',
    'pyramid_tm',
    'papyrus',
    'papyrus_ogcproxy',
    'httplib2',
    'Babel',
    'pyramid_formalchemy',
    'fa.jquery',
    'GeoFormAlchemy',
    'OWSLib',
    'tileforge',
    ]

setup(name='c2cgeoportal',
      version='0.2',
      description='c2cgeoportal',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='camptocamp',
      author_email='info@camptocamp.com',
      url='http://www.camptocamp.com/geospatial-solutions',
      keywords='web gis geoportail c2cgeoportal geocommune pyramid',
      packages=find_packages(),
      include_package_data=True,
      message_extractors={'c2cgeoportal': [
          ('static/**', 'ignore', None),
          ('**.py', 'python', None),
          ('templates/**', 'mako', {'input_encoding': 'utf-8'})]},
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="c2cgeoportal",
      entry_points = {
        'console_scripts': [
            'print_tpl = c2cgeoportal.scripts.print_tpl:main',
            'manage_db = c2cgeoportal.scripts.manage_db:run',
        ],
      }
)

