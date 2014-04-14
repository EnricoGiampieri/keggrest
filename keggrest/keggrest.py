# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division	

from compatibility import unicode

from itertools import chain, groupby
from collections import defaultdict

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
    data = RESTrequest(u'link', db1, db2, **kwargs)
    data = [tuple(d.split(u'\t')) for d in data.split(u'\n')][:-1]
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    for element_1, element_2 in data:
        rel_inv[element_1].append(element_2)
        rel_dir[element_2].append(element_1)
    return rel_dir, rel_inv


def KEGGconv(db1, db2, **kwargs):
    data = RESTrequest(u'conv', db1, db2, **kwargs)
    data = [tuple(d.split(u'\t')) for d in data.split(u'\n')][:-1]
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    for element_1, element_2 in data:
        rel_inv[element_1].append(element_2)
        rel_dir[element_2].append(element_1)
    return rel_dir, rel_inv


def KEGGlist(db, organism=u'', **kwargs):
    data = RESTrequest(u'list', db, organism, **kwargs)
    data = [tuple(d.split(u'\t')) for d in data.split(u'\n')][:-1]
    return dict(data)


def KEGGget(element, option=u'', **kwargs):
    # options = aaseq | ntseq | mol | kcf | image | kgml
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
    path_brite = RESTrequest(u'get', britename)
    BRITE = {}
    lines = path_brite.splitlines()
    for line in lines:
        key = line[0]
        line = line[1:].strip()
        if key == u'A':
            BRITE_sub = {}
            BRITE[line] = BRITE_sub
        if key == u'B':
            BRITE_sub_sub = {}
            BRITE_sub[line] = BRITE_sub_sub
        if key == u'C':
            map_key, name = line.split(' ', 1)
            BRITE_sub_sub[map_key] = name
    info = u"\n".join(
        line[1:] for line in path_brite.splitlines() if line[0] == u'#')
    return BRITE, info
