from setuptools import setup

package_name = 'nxp_cup_vision'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Benjamin Perseghetti',
    author_email='bperseghetti@rudislabs.com',
    maintainer='Benjamin Perseghetti',
    maintainer_email='bperseghetti@rudislabs.com',
    description='NXP Cup track vision ROS2',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "nxp_track_vision = nxp_cup_vision.nxp_track_vision:main"
        ],
    },
)
