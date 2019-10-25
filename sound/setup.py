from setuptools import setup


package_name = 'sound'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        "talker",
        "listener"
    ],
    data_files=[
        ('share/' + package_name, ['package.xml', 'test.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='MATSUDAYamato', 'YAMAMOTOYuuka',
    author_email='is0476hv@ed.ritsumei.ac.jp', 'rr0113ke@ed.ritsumei.ac.jp',
    maintainer='MATSUDAYamato',
    maintainer_email='is0476hv@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='sound system is made using ROS2.',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker=talker:main',
            'listener=listener:main',
        ],
    },
)
