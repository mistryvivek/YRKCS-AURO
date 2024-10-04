from setuptools import find_packages, setup
import os 
import glob

package_name = 'autodrive_with_rviz'

setup(
    name='autodrive_with_rviz',
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['launch/autodrive_with_rviz.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='auro',
    maintainer_email='auro@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
