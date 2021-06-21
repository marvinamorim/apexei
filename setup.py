from setuptools import setup

setup(
    name="apexei",
    version='0.1',
    py_modules=['apexei'],
    install_requires=[
        'click',
        'dynaconf'
    ],
    entry_points='''
        [console_scripts]
        apexei=main:apex_ei
    ''',
)