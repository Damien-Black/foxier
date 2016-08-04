from setuptools import setup


def readme():
    with open('Docs\Readme.md') as f:
        return f.read()

setup(name='foxier',
      version='0.1',
      description='Outfox even the smartest fox',
      author='Steve Osazuwa',
      author_email='sosazuwa00@gmail.com',
      license='MIT',
      packages=['foxier', 'dictionaryMaker'],
      zip_safe=False)
