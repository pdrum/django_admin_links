from distutils.core import setup

setup(
    name='django_admin_links',
    packages=['django_admin_links'],
    version='0.1',
    description='Read-only link representation of foreign keys in django admin',
    author='Pedram Hajesmaeeli',
    author_email='pedram.esmaeeli@gmail.com',
    url='https://github.com/pdrum/django_admin_links',
    keywords=['django', 'admin', 'foreign keys'],  # arbitrary keywords
    classifiers=[],
    install_requires=['django>=1.6']
)
