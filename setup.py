from distutils.core import setup

from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='socials_api',
    version='0.1',
    packages=['socials_api',
              'socials_api.twitter_api', 'socials_api.instagram_api',
              'socials_api.meta_extractor', 'socials_api.facebook_api'],
    url='',
    license='',
    author='Raphaaël Courivaud',
    author_email='r.courivaud@gmail.com',
    description='',
    install_requires=reqs

)
