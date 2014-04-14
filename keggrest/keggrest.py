# -*- coding: utf-8 -*-
from itertools import chain, groupby
from collections import defaultdict
import urllib2
import pickle


def print_verbose(verbose, text):
    if verbose:
        print text


def RESTrequest(*args, **kwargs):
    """return and save the blob of data that is returned
    from kegg without caring to the format"""
    verbose = kwargs.get('verbose', False)
    force_download = kwargs.get('force', False)
    save = kwargs.get('force', True)

    # so you can copy paste from kegg
    args = list(chain.from_iterable(a.split('/') for a in args))
    args = [a for a in args if a]
    request = 'http://rest.kegg.jp/' + "/".join(args)
    print_verbose(verbose, "richiedo la pagina: " + request)
#    filename = "KEGG_" + "_".join(args)
#    try:
#        if force_download:
#            raise IOError()
#        print_verbose(verbose, "loading the cached file " + filename)
#        with open(filename, 'r') as f:
#            data = pickle.load(f)
#    except IOError:
    print_verbose(verbose, "downloading the library,it may take some time")
    
    try:
        req = urllib2.urlopen(request)
        data = req.read()
#        if save:
#            with open(filename, 'w') as f:
#                print_verbose(verbose, "saving the file to " + filename)
#                pickle.dump(data, f)
    # clean the error stacktrace
    except urllib2.HTTPError as e:
        raise e
        
    return data


def KEGGlink(db1, db2, **kwargs):
    data = RESTrequest('link', db1, db2, **kwargs)
    data = [tuple(d.split('\t')) for d in data.split('\n')][:-1]
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    for element_1, element_2 in data:
        rel_inv[element_1].append(element_2)
        rel_dir[element_2].append(element_1)
    return rel_dir, rel_inv


def KEGGconv(db1, db2, **kwargs):
    data = RESTrequest('conv', db1, db2, **kwargs)
    data = [tuple(d.split('\t')) for d in data.split('\n')][:-1]
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    for element_1, element_2 in data:
        rel_inv[element_1].append(element_2)
        rel_dir[element_2].append(element_1)
    return rel_dir, rel_inv


def KEGGlist(db, organism='', **kwargs):
    data = RESTrequest('list', db, organism, **kwargs)
    data = [tuple(d.split('\t')) for d in data.split('\n')][:-1]
    return dict(data)


def KEGGget(element, option='', **kwargs):
    # options = aaseq | ntseq | mol | kcf | image | kgml
    data = RESTrequest('get', element, option, **kwargs)
    data = data.split('\n')
    grouped = list(l.split(' ', 1) for l in data)
    grouped = [l for l in grouped if len(l) > 1]
    result = defaultdict(list)
    last_key = None
    for key, value in grouped:
        if key.strip():
            last_key = key.strip()
        result[last_key].append(value.strip())
    return result


def KEGGbrite(britename, option='', **kwargs):
    path_brite = RESTrequest('get', britename)
    BRITE = {}
    lines = path_brite.splitlines()
    for line in lines:
        key = line[0]
        line = line[1:].strip()
        if key == 'A':
            BRITE_sub = {}
            BRITE[line] = BRITE_sub
        if key == 'B':
            BRITE_sub_sub = {}
            BRITE_sub[line] = BRITE_sub_sub
        if key == 'C':
            map_key, name = line.split(' ', 1)
            BRITE_sub_sub[map_key] = name
    info = "\n".join(
        line[1:] for line in path_brite.splitlines() if line[0] == '#')
    return BRITE, info
