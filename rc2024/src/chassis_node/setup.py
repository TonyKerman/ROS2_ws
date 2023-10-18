from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'chassis_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='TonyKerman',
    maintainer_email='2676239430@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'virtual_chassis_node = chassis_node.virtual_chassis_node:main',
            'example_client = chassis_node.example_client:main'
        ],
    },
)
