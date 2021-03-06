""" Basic tests for ooxml.py """

import unittest

import os
from os.path import join, splitext
from tests.test_utils import DATA_BASE_DIR
from oletools.thirdparty.olefile import isOleFile
from oletools import ooxml


class TestOOXML(unittest.TestCase):
    """ Tests my cool new feature """

    DO_DEBUG = False

    def test_all_rough(self):
        """Checks all samples, expect either ole files or good ooxml output"""
        acceptable = ooxml.DOCTYPE_EXCEL, ooxml.DOCTYPE_WORD, \
                     ooxml.DOCTYPE_POWERPOINT

        # files that are neither OLE nor xml:
        except_files = 'empty', 'text'
        except_extns = '.xml', '.rtf', '.csv'

        # analyse all files in data dir
        for base_dir, _, files in os.walk(DATA_BASE_DIR):
            for filename in files:
                if filename in except_files:
                    if self.DO_DEBUG:
                        print('skip file: ' + filename)
                    continue
                if splitext(filename)[1] in except_extns:
                    if self.DO_DEBUG:
                        print('skip extn: ' + filename)
                    continue

                full_name = join(base_dir, filename)
                if isOleFile(full_name):
                    if self.DO_DEBUG:
                        print('skip ole: ' + filename)
                    continue
                try:
                    doctype = ooxml.get_type(full_name)
                except Exception:
                    self.fail('Failed to get doctype of {0}'.format(filename))
                self.assertTrue(doctype in acceptable,
                                msg='Doctype "{0}" for {1} not acceptable'
                                    .format(doctype, full_name))
                if self.DO_DEBUG:
                    print('ok: {0} --> {1}'.format(filename, doctype))


# just in case somebody calls this file as a script
if __name__ == '__main__':
    unittest.main()
