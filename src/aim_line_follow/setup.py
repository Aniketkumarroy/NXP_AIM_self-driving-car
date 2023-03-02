from setuptools import setup

package_name = 'aim_line_follow'

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
    maintainer='Landon Haugh',
    maintainer_email='landon.haugh@nxp.com',
    description='Line follower for NXP Gazebo simulation (AIM Version)',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'line_follower = aim_line_follow.aim_line_follow:main',
        ],
    },
)
