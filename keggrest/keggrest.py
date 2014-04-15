# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division	

"""
Database 	Name 	Abbrev 	kid 	Remark
KEGG PATHWAY 	pathway 	path 	map number 	
KEGG BRITE 	brite 	br 	br number 	
KEGG MODULE 	module 	md 	M number 	
KEGG DISEASE 	disease 	ds 	H number 	Japanese version: disease_ja ds_ja
KEGG DRUG 	drug 	dr 	D number 	Japanese version: drug_ja dr_ja
KEGG ENVIRON 	environ 	ev 	E number 	Japanese version: environ_ja ev_ja
KEGG ORTHOLOGY 	orthology 	ko 	K number 	
KEGG GENOME 	genome 	genome 	T number 	
KEGG GENOMES 	genomes 	gn 	T number 	Composite database: genome + egenome + mgenome
KEGG GENES 	genes 	- 	- 	Composite database: consisting of KEGG organisms
KEGG LIGAND 	ligand 	ligand 	- 	Composite database: compound + glycan + reaction + rpair + rclass + enzyme
KEGG COMPOUND 	compound 	cpd 	C number 	Japanese version: compound_ja cpd_ja
KEGG GLYCAN 	glycan 	gl 	G number 	
KEGG REACTION 	reaction 	rn 	R number 	
KEGG RPAIR 	rpair 	rp 	RP number 	
KEGG RCLASS 	rclass 	rc 	RC number 	
KEGG ENZYME 	enzyme 	ec 	-
"""

from compatibility import unicode

from itertools import chain, groupby, takewhile, dropwhile, islice
from collections import defaultdict
from string import ascii_uppercase

#python 2 & 3 compatibility layer
try:
    from urllib2 import urlopen, HTTPError
except ImportError:
    from urllib.request import urlopen
    from urllib.error import HTTPError
    

def print_verbose(verbose, text):
    if verbose:
        print(text)

def RESTrequest(*args, **kwargs):
    """return and save the blob of data that is returned
    from kegg without caring to the format
    
    cache should be a mappable where the results of the query are stored
    """
    
    cache = kwargs.get(u'cache', None)
    # so you can copy paste from kegg
    args = list(chain.from_iterable(a.split(u'/') for a in args))
    args = [a for a in args if a]
    request = u'http://rest.kegg.jp/' + u"/".join(args)
    def ulr_request():
        try:
            req = urlopen(request)
            data = req.read()
        except HTTPError as e:
            raise e
        return unicode(data)
        
    if cache is not None:
        if request not in cache:
            data = ulr_request()
            cache[request] = data
        else:
            data = cache[request]
    else:
        data = ulr_request()
    return data


def KEGGlink(db1, db2, **kwargs):
    """link the content of two different databases.
    
    it returns two dictionaries, giving the direct and inverse linkage 
    between the two databases
    
    use the keyword cache with a mapping to use a cache of the downloaded data    
    
    ===
    USAGE
    ===

    http://rest.kegg.jp/link/<target_db>/<source_db>

    <target_db> = <database>
    <source_db> = <database>
    <database> = pathway | brite | module | disease | drug | 
                 environ | ko | genome | <org> | compound | glycan |
                 reaction | rpair | rclass | enzyme    
    
    http://rest.kegg.jp/link/<target_db>/<dbentries>
    <dbentries> = KEGG database entries involving the following <database>
    <database> = pathway | brite | module | disease | drug | environ | ko |
                 genome | <org> | compound | glycan | reaction | rpair |
                 rclass | enzyme | genes    
    
    ===
    EXAMPLES
    ===
    
    /link/pathway/hsa 	  	
        KEGG pathways linked from each of the human genes
    /link/hsa/pathway 	  	
        human genes linked from each of the KEGG pathways
    /link/pathway/hsa:10458+ece:Z5100 	  	
        KEGG pathways linked from a human gene and an E. coli O157 gene
    /link/genes/K00500 	  	
        List of genes with the KO assignment of K00500
    /link/genes/hsa00010
    /link/hsa/hsa00010 	  	
        List of human genes in pathway hsa00010
    /link/ko/map00010 or /link/ko/ko00010 	  	
        List of KO entries in pathway map00010 or ko00010
    /link/rn/map00010 or /link/rn/rn00010 	  	
        List of reaction entries in pathway map00010 or rn00010
    /link/ec/map00010 or /link/ec/ec00010 	  	
        List of EC number entries in pathway map00010 or ec00010
    /link/cpd/map00010 	  	
        List of compound entries in pathway map00010 
    """
    
    data = RESTrequest(u'link', db1, db2, **kwargs)
    data = [tuple(d.split(u'\t')) for d in data.split(u'\n')][:-1]
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    for element_1, element_2 in data:
        rel_inv[element_1].append(element_2)
        rel_dir[element_2].append(element_1)
    return rel_dir, rel_inv


def KEGGlist(db, organism=u'', **kwargs):
    """link the content of a specific database

    it returns a dictionary containing the database entries description
    
    ===
    USAGE
    ===
    
    http://rest.kegg.jp/list/<database>
    <database> = pathway | brite | module | disease | drug | environ | ko | genome |
                 <org> | compound | glycan | reaction | rpair | rclass | enzyme |
                 organism
    <org> = KEGG organism code or T number
    
    http://rest.kegg.jp/list/<database>/<org>
    <database> = pathway | module
    <org> = KEGG organism code
    
    http://rest.kegg.jp/list/<dbentries>
    <dbentries> = KEGG database entries involving the following <database>
    <database> = pathway | brite | module | disease | drug | environ | ko | genome |
                 <org> | compound | glycan | reaction | rpair | rclass | enzyme
    <org> = KEGG organism code or T number
    
    ===
    EXAMPLES
    ===
    
    /list/pathway 	  	
        returns the list of reference pathways
    /list/pathway/hsa 	  	
        returns the list of human pathways
    /list/organism 	  	
        returns the list of KEGG organisms with taxonomic classification
    /list/hsa 	  	
        returns the entire list of human genes
    /list/T01001 	  	
        same as above
    /list/hsa:10458+ece:Z5100 	  	
        returns the list of a human gene and an E.coli O157 gene
    /list/cpd:C01290+gl:G00092 	  	
        returns the list of a compound entry and a glycan entry
    /list/C01290+G00092 	  	
        same as above 
    
    """
    
    data = RESTrequest(u'list', db, organism, **kwargs)
    data = [tuple(d.split(u'\t')) for d in data.split(u'\n')][:-1]
    return dict(data)



def KEGGconv(db1, db2, **kwargs):
    """convert an element to or from an outside database
    
    ===
    USAGE
    ===
    
    http://rest.kegg.jp/conv/<target_db>/<source_db>

    (<target_db> <source_db>) = (<kegg_db> <outside_db>) | (<outside_db> <kegg_db>)
    
    For gene identifiers:
    <kegg_db> = <org>
    <org> = KEGG organism code or T number
    <outside_db> = ncbi-gi | ncbi-geneid | uniprot
    
    For chemical substance identifiers:
    <kegg_db> = drug | compound | glycan
    <outside_db> = pubchem | chebi
    
    http://rest.kegg.jp/conv/<target_db>/<dbentries>
    
    For gene identifiers:
    <dbentries> = database entries involving the following <database>
    <database> = <org> | genes | ncbi-gi | ncbi-geneid | uniprot
    <org> = KEGG organism code or T number
    
    For chemical substance identifiers:
    <dbentries> = database entries involving the following <database>
    <database> = drug | compound | glycan | pubchem | chebi
    
    ===
    EXAMPLE
    ===
    
    /conv/eco/ncbi-geneid 	  	
        conversion from NCBI GeneID to KEGG ID for E. coli genes
    /conv/ncbi-geneid/eco 	  	
        opposite direction
    /conv/ncbi-gi/hsa:10458+ece:Z5100 	  	
        conversion from KEGG ID to NCBI GI
    /conv/genes/ncbi-gi:3113320 	  	
        conversion from NCBI GI to KEGG ID when the organism code is not known
    
    """
    data = RESTrequest(u'conv', db1, db2, **kwargs)
    data = [tuple(d.split(u'\t')) for d in data.split(u'\n')][:-1]
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    for element_1, element_2 in data:
        rel_inv[element_1].append(element_2)
        rel_dir[element_2].append(element_1)
    return rel_dir, rel_inv



def KEGGget(element, option=u'', **kwargs):
    """retrieve an element from a  database
    
    currently it doesn't work when options are used
    ===
    USAGE
    ===
    http://rest.kegg.jp/get/<dbentries>[/<option>]
    <dbentries> = KEGG database entries involving the following <database>
    <database> = pathway | brite | module | disease | drug | environ | ko | genome |
                 <org> | compound | glycan | reaction | rpair | rclass | enzyme
    <org> = KEGG organism code or T number
    
    <option> = aaseq | ntseq | mol | kcf | image | kgml

    ===
    EXAMPLE
    ===
    
    /get/cpd:C01290+gl:G00092 	  	
        retrieves a compound entry and a glycan entry
    /get/C01290+G00092 	  	
        same as above
    /get/hsa:10458+ece:Z5100 	  	
        retrieves a human gene entry and an E.coli O157 gene entry
    /get/hsa:10458+ece:Z5100/aaseq 	  	
        retrieves amino acid sequences of a human gene and an E.coli O157 gene
    /get/hsa05130/image 	  	
        retrieves the image file of a pathway map
    /get/hsa05130/kgml 	  	
        retrieves the kgml file of a pathway map
    """
    data = RESTrequest(u'get', element, option, **kwargs)
    data = data.split(u'\n')
    grouped = list(l.split(u' ', 1) for l in data)
    grouped = [l for l in grouped if len(l) > 1]
    result = defaultdict(list)
    last_key = None
    for key, value in grouped:
        if key.strip():
            last_key = key.strip()
        result[last_key].append(value.strip())
    return result


def KEGGbrite(britename, option='', **kwargs):
    """
    list of available brites:
        keggrest.RESTrequest('list', 'brite', cache=cache)

    get a specific one:

        keggrest.KEGGbrite('br:br08901', cache=cache)
    """
    britename = 'br:br08302_enzyme'
    path_brite = RESTrequest(u'get', britename, **kwargs)
    
    i = iter(path_brite.splitlines())
    i = dropwhile(lambda l: not l.startswith('!'), i)
    i = islice(i, 1, None)
    i = takewhile(lambda l: not l.startswith('!'), i)
    lines = list(i)    
    
    #print '\n'.join(l.replace('  ', '\t') for l in lines[:30])  
    letter_index = dict([(l,i) for i, l in enumerate(ascii_uppercase)])
    from collections import OrderedDict
    dict_class = OrderedDict    
    
if True: 
    dictionary_level = [dict_class()]
    last_index_level = 0
    last_line = None
    for idx, line in enumerate(lines):
        key = line[0]
        print idx, key
        line = line[1:].strip()
        new_index = letter_index[key]
        if new_index==last_index_level:
            print "same level"
            print new_index, last_index_level
            print line, last_line
            print
            # add a new key into the structure
            a = dict_class()
            dictionary_level[last_index_level][line] = a
            dictionary_level.append(a)
            last_line = line
            last_index_level = new_index
    
        elif new_index==last_index_level+1:
            print "downward level"
            print new_index, last_index_level
            print line, last_line
            print
            #deepen the structure
            a = dictionary_level[last_index_level][last_line]
            a[line] = dict_class()
            dictionary_level.append(a[line])
            last_line = line
            last_index_level = new_index
            
        elif new_index<last_index_level:
            print "upward level"
            print new_index, last_index_level
            print line, last_line
            print
            # run to an upper level
            dictionary_level = dictionary_level[:new_index+1]
            a = dictionary_level[-1]
            a[line] = dict_class()
            dictionary_level.append(a[line])
            last_line = line
            last_index_level = new_index
    
    BRITE = dictionary_level[0]
    #info = u"\n".join(line[1:] for line in path_brite.splitlines() if line[0] == u'#')
    return BRITE#, info
