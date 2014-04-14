# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division	

"""
Created on Mon Apr 14 11:52:46 2014

@author: enrico.giampieri2
"""

from compatibility import *

import keggrest
import unittest

class SimplisticTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
    
    def test_keggrest_run_1(self):
        data = keggrest.RESTrequest('get', 'path:hsa00232')
        self.assertTrue(data is not None)
##
#if __name__ == "__main__":
#    # get the data out of a definition
#    data = KEGGget('path:hsa00232')
#    print data.keys()
#
#if __name__ == "__main__":
#    # list of human pathway
#    data_path_defs = KEGGlist('pathway', 'hsa')
#    print len(data_path_defs), data_path_defs.items()[0]
#
#if __name__ == "__main__":
#    # list of human genes
#    data_gene_defs = KEGGlist('hsa')
#    print len(data_gene_defs), data_gene_defs.items()[0]
#
#if __name__ == "__main__":
#    # list of compounds
#    data_comp_defs = KEGGlist('compound')
#    print len(data_comp_defs), data_comp_defs.items()[0]
#
#if __name__ == "__main__":
#    # list of reactions
#    data_reac_defs = KEGGlist('reaction')
#    print len(data_reac_defs), data_reac_defs.items()[0]
#
#if __name__ == "__main__":
#    # list of reaction couples
#    data_rpair_defs = KEGGlist('rpair')
#    print len(data_rpair_defs), data_rpair_defs.items()[0]
#
#if __name__ == "__main__":
#    # link between human genes and pathways
#    data_lph, data_lhp = KEGGlink('pathway', 'hsa')
#    print len(data_lph), data_lph.items()[0]
#    print len(data_lhp), data_lhp.items()[0]
#
#if __name__ == "__main__":
#    # which genes are related to which reactions
#    data_lrh, data_lhr = KEGGlink('reaction', 'hsa')
#    print len(data_lrh), data_lrh.items()[0]
#    print len(data_lhr), data_lhr.items()[0]
#
#if __name__ == "__main__":
#    # which genes are related to which compounds
#    data_lch, data_lhc = KEGGlink('compound', 'hsa')
#    print len(data_lch), data_lch.items()[0]
#    print len(data_lhc), data_lhc.items()[0]
#
#if __name__ == "__main__":
#    # which modules are related to which pathway
#    data_lmp, data_lpm = KEGGlink('module', 'hsa')
#    print len(data_lmp), data_lmp.items()[0]
#    print len(data_lpm), data_lpm.items()[0]
#
#if __name__ == "__main__":
#    # which genes are related to which reactions
#    data_lrp, data_lpr = KEGGlink('reaction', 'pathway')
#    print len(data_lrp), data_lrp.items()[0]
#    print len(data_lpr), data_lpr.items()[0]

    
if __name__ == '__main__':
    unittest.main()