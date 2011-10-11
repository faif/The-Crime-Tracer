try:
    import constants
    from borg import Borg
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

# seperate check because lxml is not available on all platforms
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

__all__ = ['ConfigParser']

class ConfigParser(Borg):

    def __init__(self, fullname, xmlns):
        try:
            self.cfg = etree.parse(fullname)
        except IOError as err:
            import os
            path = os.path.basename(__file__)
            raise SystemExit("{0}: couldn't load config file: {1}".format(path, fullname))

        self.xmlns = xmlns
        self.root = self.cfg.getroot()

    def all_matches(self, name):
        '''Get a list of the elements matching name'''
        xml_name = ('.//', '{', self.xmlns, '}', name)
        return self.cfg.findall(''.join(xml_name))

    def first_match(self, name):
        '''Get the first element that matches with name'''
        xml_name = ('.//', '{', self.xmlns, '}', name)
        return self.cfg.find(''.join(xml_name))

if __name__ == '__main__':
    cp = ConfigParser('tct.xml', constants.CFG_XMLNS)
    print([i.text for i in cp.all_matches('slide')])
    print(cp.first_match('bg').text)
    print(cp.first_match('graphics').attrib)
