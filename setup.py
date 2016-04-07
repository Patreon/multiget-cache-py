from setuptools import setup, find_packages

setup(name='multiget-cache',
      version='0.0.2',
      description='Python library for turning N O(1) function calls into 1 O(1) call.',
      url='http://github.com/Patreon/multiget-cache-py',
      author='Patreon',
      author_email='zach@patreon.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      zip_safe=True)
