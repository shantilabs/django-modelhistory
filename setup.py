from distutils.core import setup


setup(
    name='modelhistory',
    version='0.1',
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    packages=[
        'modelhistory',
    ],
    url='https://github.com/shantilabs/django-modelhistory',
    requires=['django', 'pymongo >= 1.1.1'],
)
