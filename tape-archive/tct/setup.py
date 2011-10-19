from distutils.core import setup

setup(
    name = 'tct',
    packages = ['src'],         # TODO: rename to tct
    version = '1.0',
    description = 'A classic 2D adventure crime game',
    author = 'Free Software Gaming Geeks',
    author_email = 'fsgamedev@googlegroups.com',
    url = 'https://gitorious.org/the-crime-tracer',
    download_url = 'https://gitorious.org/the-crime-tracer/tct-developers/archive-tarball/dev',
    keywords = ['adventure', '2D', 'crime'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Operating System :: OS Independent'
        ],
    long_description = '''The Crime Tracer (tct) is a classic 2D adventure crime game. The main 
                          character of the game is a detective who is investigating several crime 
                          cases while trying to arrest a professional serial killer...'''
    )
