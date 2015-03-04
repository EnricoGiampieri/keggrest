# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 11:52:46 2014

@author: enrico.giampieri2
"""
from __future__ import absolute_import, unicode_literals, print_function

import unittest

import responses

import keggrest

# %%


class test_RequestGeneration(unittest.TestCase):
    def test_correct_request(self):
        pieces = ['link', 'pathway', 'hsa']
        req = keggrest._generate_keggrest_request(*pieces)
        epected = 'http://rest.kegg.jp/link/pathway/hsa'
        self.assertEqual(req, epected)

    def test_wrong_action(self):
        pieces = ['peach', 'pathway', 'hsa']
        with self.assertRaises(ValueError):
            keggrest._generate_keggrest_request(*pieces)


# %%
class test_Utilities(unittest.TestCase):
    def test_split_lines_1(self):
        data = """
        one\ttwo

        three\tfour
        """
        new_data = keggrest._split_lines(data)
        expected = [('one', 'two'), ('three', 'four')]
        self.assertEqual(new_data, expected)

    def test_split_lines_void_1(self):
        data = ""
        new_data = keggrest._split_lines(data)
        expected = []
        self.assertEqual(new_data, expected)

    def test_split_lines_void_2(self):
        data = """\t
        """
        new_data = keggrest._split_lines(data)
        expected = []
        self.assertEqual(new_data, expected)

    # %% double_way_hashtable
    def test_double_way_hashtable_no_link(self):
        data = ''
        data = keggrest._split_lines(data)
        dict_dir, dict_inv = keggrest._double_way_hashtable(data)
        self.assertEqual(dict_dir, {})
        self.assertEqual(dict_inv, {})

    def test_double_way_hashtable_single_link(self):
        data = """
               path:path0000 \t hsa:hsa000001
               """
        data = keggrest._split_lines(data)
        dict_dir, dict_inv = keggrest._double_way_hashtable(data)
        self.assertEqual(dict_dir, {'path:path0000': ['hsa:hsa000001']})
        self.assertEqual(dict_inv, {'hsa:hsa000001': ['path:path0000']})

    def test_double_way_hashtable_double_link_first(self):
        data = """
               path:path0000 \t hsa:hsa000001
               path:path0000 \t hsa:hsa000002
               """
        data = keggrest._split_lines(data)
        dict_dir, dict_inv = keggrest._double_way_hashtable(data)
        self.assertEqual(dict_dir, {'path:path0000': ['hsa:hsa000001',
                                                      'hsa:hsa000002']})
        self.assertEqual(dict_inv, {'hsa:hsa000001': ['path:path0000'],
                                    'hsa:hsa000002': ['path:path0000']})

    def test_double_way_hashtable_double_link_second(self):
        data = """
               path:path0000 \t hsa:hsa000001
               path:path0001 \t hsa:hsa000001
               """
        data = keggrest._split_lines(data)
        dict_dir, dict_inv = keggrest._double_way_hashtable(data)
        self.assertEqual(dict_dir, {'path:path0000': ['hsa:hsa000001'],
                                    'path:path0001': ['hsa:hsa000001']})
        self.assertEqual(dict_inv, {'hsa:hsa000001': ['path:path0000',
                                                      'path:path0001']})

    def test_double_way_hashtable_invalid(self):
        data = """
               path:path0000
               """
        with self.assertRaises(ValueError) as cm:
            data = keggrest._split_lines(data)
            dict_dir, dict_inv = keggrest._double_way_hashtable(data)
        expected = ("the line need to have two elements to be split,"
                    " received: ('path:path0000',)")
        obtained = str(cm.exception)
        self.assertEqual(obtained, expected)
# %%

###############################################################################
#                   LOW LEVEL API                                             #
###############################################################################
kegg_url = u'http://rest.kegg.jp'


class test_Keggrest(unittest.TestCase):
    # %% KEGGlist
    @responses.activate
    def test_KEGGlist_1_element(self):

        responses.add(responses.GET,
                      kegg_url+u'/list/pathway/',
                      body="""
                           path:path0000\ttest path
                           """)
        data = keggrest.KEGGlist('pathway')
        self.assertTrue(data is not None)
        self.assertEqual(data, {'path:path0000': 'test path'})

    @responses.activate
    def test_KEGGlist_0_element(self):
        responses.add(responses.GET,
                      kegg_url+u'/list/pathway/',
                      body="""
                           """)
        data = keggrest.KEGGlist('pathway')
        self.assertTrue(data is not None)
        self.assertEqual(data, {})

    @responses.activate
    def test_KEGGlist_2_element(self):
        responses.add(responses.GET,
                      kegg_url+u'/list/pathway/',
                      body="""
                           path:path0000\ttest path 1
                           path:path0001\ttest path 2
                           """)
        data = keggrest.KEGGlist('pathway')
        self.assertTrue(data is not None)
        expected = {'path:path0000': 'test path 1',
                    'path:path0001': 'test path 2',
                    }
        self.assertEqual(data, expected)



if __name__ == '__main__':
    unittest.main()