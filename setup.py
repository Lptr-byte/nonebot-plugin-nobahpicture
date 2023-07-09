import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nonebot-plugin-nobahpictrue',
    version='1.0.0',
    author='Hansa',
    author_email='hanasakayui2022@gmail.com',
    description='获取碧蓝档案涩图',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    install_requires=['requests==2.25.1'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    )
)
