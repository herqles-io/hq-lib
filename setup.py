from setuptools import setup, find_packages

setup(
    name='hq-lib',
    version='2.0.0-dev',
    url='https://github.com/herqles-io/hq-lib',
    include_package_data=True,
    license='MIT',
    author='CoverMyMeds',
    description='Herqles Library',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'pika==0.9.14',
        'enum34==1.0.4',
        'sqlalchemy==1.0.8',
    ],
    extras_require={
        'ldap': ['python-ldap==2.4.*']
    },
)
