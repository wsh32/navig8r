from setuptools import setup

try:  # pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # pip <= 9.0.2
    from pip.req import parse_arguments

setup(
    name='navig8r',
    version='v0.0-beta',
    packages=[''],
    package_dir={'', 'navig8r',},
    url='https://github.com/wsh32/navig8r',
    license='MIT',
    author='',
    author_email='',
    description='Make Harvard 2020',
    install_requires=[str(r.req) for r in parse_requirements('requirements.txt', session='hack')]
)
