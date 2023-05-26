from setuptools import setup

package_name = 'ROS2_FreshmanProject'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'serial_node = ROS2_FreshmanProject.Serial:main',
            'servo_node = ROS2_FreshmanProject.Servo:main',
            'mpu_node = ROS2_FreshmanProject.Mpu:main',
        ],
    },
)
