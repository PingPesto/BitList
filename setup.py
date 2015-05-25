import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid-mongoengine',
    'waitress',
    'python-mpd2',
    'youtube-dl',
    'rq',
    'path.py',
    'boto',
    'tinys3',
    'honcho',
    'spotify-ripper',
    'cryptacular',
    ]

setup(name='bitlist',
      version='0.0',
      description='bitlist',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="bitlist",
      entry_points="""\
      [paste.app_factory]
      main = bitlist:main
      [console_scripts]
      initialize_bitlist_db = bitlist.scripts.initializedb:main
      """,
      )
