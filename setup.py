from setuptools import setup, find_packages

setup(
    name='hq-lib',
    version='1.0.0',
    url='',
    include_package_data=True,
    license='',
    author='Ryan Belgrave',
    author_email='rbelgrave@covermymeds.com',
    description='Herqles Library',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'pika==0.9.14',
        'enum34==1.0.4',
        'sqlalchemy==1.0.4',
    ],
    extras_require={
        'ldap': ['python-ldap==2.4.19']
    },
)
