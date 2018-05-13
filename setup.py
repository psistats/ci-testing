from setuptools import setup

setup(name='citest',
      version='0.1.0.dev8',
      description='A project to test ci and building',
      author='Alex Dow',
      author_email='adow@psikon.com',
      url='http://github.com/psistats/ci-testing',
      packages=['citest'],
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      python_requires='>=3.5'

)