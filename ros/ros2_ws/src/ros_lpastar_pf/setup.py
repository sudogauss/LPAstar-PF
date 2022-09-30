from setuptools import setup

package_name = 'ros_lpastar_pf'

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
    maintainer='Tim L.',
    maintainer_email='t.liashkevich1772@gmail.com',
    description='Path finder node based on LPA* algorithm using two clients: one for client\'s instructions communication and the other for scan data.',
    license='GNU GPLv3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
