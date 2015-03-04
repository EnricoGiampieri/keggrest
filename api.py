# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division	
"""
Created on Tue Apr 15 11:41:05 2014

@author: enrico.giampieri2
"""


# don't be and architect astronaut, keep it down to earth
# consistency, stick with conventional
# brevity
# composability, minimize the assumptions
# plain data, avoid strange data structures and mind the data type used
# grooviness, drive the user on the right path
# safety

from compatibility import unicode

from functools import partial
import pickle

import keggrest

class _OrganismWrapper(object):
    def __init__(son, database, organism_code):
        son.database = database
        son.code = organism_code
        
    def __getattr__(son, func_name):
        return partial(son.database.__getattribute__(func_name), son.code)
    
    @property
    def info(son):
        return son.database.get_info(son.code)
        
    def __repr__(self):
        return self.info
        
    def __str__(self):
        return self.info
    
    @property
    def genes(son):
        return son.database.get_genes(son.code)
        
    @property
    def pathways(son):
        return son.database.get_pathways(son.code)

################################################################

################################################################

class Database(dict):
    def __init__(self, cache=None):
        """create a proxy for the KEGG database.
        
        It will take an optional (reccomended) argument cache.
        If it's None it will use simply internal caching to reduce 
        the number of calls to the KEGG rest api.
        An external mapping can be used, that allows for a more
        refined control of the caching procedure.
        """
        self.cache = {} if cache is None else cache
        self.organisms = self.get_organisms()
        self.organisms_short = {org_short for (org_short, org_name, org_taxo) 
                                                in self.organisms.values()}
        
        for org_short in self.organisms_short:
            #create shortcuts for all organisms
            self[org_short] = _OrganismWrapper(self, org_short)
            
    @property
    def info(self):
        """information about the whole kegg database
        """
        return self.get_info('kegg')
    
    def check_valid_organism(self, organism):
        if organism not in self.organisms_short:
            e = 'organism "{}" not present in the KEGG database'
            raise ValueError(e.format(organism))
        return True
    
    
    def get_info(self, object_code):
        """return the info on a requested object
        
        it will not format the information, as any object has its
        own formatting
        """
        infos = keggrest.RESTrequest(u'info', object_code, cache=self.cache)
        return infos
        
        
    def dump(self, filename):
        """dump the database into a file, ready for future readings
        """
        with open(filename,'w') as destination:
            pickle.dump(self.cache, destination)
        
    def get_organisms(self):
        """get the complete dictionary of all organisms
        
        the dictionary has the organism code as keys and as values:
            organism short name
            organism complete name
            tuple of organism taxonomical classification
        """
        organisms_text = keggrest.RESTrequest(u'list',
                                     u'organism',
                                     cache=self.cache)
        organisms = {}
        for pieces in keggrest.split_lines(organisms_text):
            org_code, org_short, org_name, org_phylo = pieces
            organisms[org_code] = org_short, org_name, org_phylo.split(';')
        return organisms
        
    def get_genes(self, organism=u'hsa'):
        """try to download all the genes from kegg for a given organism
        
        raise a ValueError if the organism doesn't exist
        """
        self.check_valid_organism(organism)
        genes = keggrest.KEGGlist(organism, cache=self.cache)
        return genes
        
    def get_pathways(self, organism=u'hsa'):
        """try to download all the genes from kegg for a given organism
        
        raise a ValueError if the organism doesn't exist
        """
        self.check_valid_organism(organism)
        pathways = keggrest.KEGGlist('pathway', organism, cache=self.cache)
        return pathways
        
    #def __getattr__(self, object_code):
    #    return _OrganismWrapper(self, object_code)
        
    def __repr__(self):
        return self.info
        
    def __str__(self):
        return self.info
    
if __name__ == '__main__':
    with open('kegg-2014-04-14.dump', 'r') as cache_file:
        cache_new = pickle.load(cache_file)
        D = Database(cache_new)
    
    #D = api.Database(cache)
    
    g1 = D.get_genes('hsa')
    g2 = D['hsa'].get_genes()
    g3 = D['hsa'].genes
    
    assert sorted(g2.keys()) == sorted(g1.keys())
    assert sorted(g2.keys()) == sorted(g3.keys())
    
    print(D['hsa'].info)
    
    print(D.info)
    
    #D.get_genes('lumacone')
    rel_path2gene, rel_gene2path = keggrest.KEGGlink(u'pathway',
                                                     u'compound',
                                                     cache=D.cache)	    
                                   
    
    from collections import defaultdict
    from itertools import combinations
    
    path_rel = defaultdict(set)
    for gene, path_pool in rel_gene2path.items():
        for path_1, path_2 in combinations(path_pool, 2):
            path_rel[path_1].add(path_2)
            path_rel[path_2].add(path_1)
    
    
    D.dump('kegg-2014-04-14.dump')
