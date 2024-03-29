from setuptools import find_packages, setup
from glob import glob
import os

#改名字 change name
package_name = 'r2_arm_test_01'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #添加文件夹
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/**')),
        (os.path.join('share', package_name), glob('*.rviz')),
        (os.path.join('share',package_name, 'meshes'),glob('meshes/*.STL'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='2676239430@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'r2_arm_display_node = r2_arm_test_01.r2_arm_display_node:main',
            'r2_arm_test_node = r2_arm_test_01.r2_arm_test_node:main',
            'client_node = r2_arm_test_01.example_client:main'
        ],
    },
)


