import os
from configparser import RawConfigParser
config__ = RawConfigParser()

def getconfigValue(seccion_, key_):
    try:
        path_config = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                   './Config', 'params.ini'))
        config__.read(path_config)
        return config__.get(seccion_, key_)
    except Exception as e:
        print(e.args[0])

# if __name__ == '__main__':
#     print(getconfigValue('PARAMS', 'url'))