from setuptools import setup, find_packages

version = '0.1.2-cirb.dev0'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('HISTORY.txt').read()
    + '\n')

setup(name='Products.BelgianEidAuthPlugin',
      version=version,
      description="",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python"
      ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone'
      ],
      extras_require={
          'test': ['plone.testing', 'plone.app.testing', 'plone.api', 'Products.PloneTestCase'],
      })
