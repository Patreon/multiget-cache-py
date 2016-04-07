from setuptools import setup, find_packages

setup(name='multiget-cache',
      version='0.0.3',
      description='Python library for turning N function calls into 1 memoized call. Especially useful for SQL optimization.',
      url='http://github.com/Patreon/multiget-cache-py',
      author='Patreon',
      author_email='zach@patreon.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      zip_safe=True)
