from setuptools import setup, find_packages

setup(
    name='foomn',
    version='0.0',
    packages=find_packages(),
    include_package_data=True,
    url='http://foo.mn/',
    license='AGPLv3',
    author='hirokiky',
    author_email='hirokiky@gmail.com',
    description='A distributed URL shortener service',
    zip_safe=False,
    install_requires=[
        'pyramid==1.4.5',
        'pyramid_debugtoolbar',
        'waitress',
        'SQLAlchemy==0.9.3',
        'pyramid_tm==0.7',
        'transaction==1.4.1',
        'zope.sqlalchemy==0.7.4',
    ],
    entry_points="""\
    [paste.app_factory]
    main = foomn:main
    [console_scripts]
    initialize_foomn_db = foomn.scripts.initializedb:main
    """,
)
