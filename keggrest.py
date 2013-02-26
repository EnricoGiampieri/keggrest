# -*- coding: utf-8 -*-
from itertools import chain, groupby
from collections import defaultdict
import pickle


def print_verbose(verbose, text):
    if verbose:
        print text


def RESTrequest(*args, **kwargs):
    """ritorna e salva il blob di dati che viene restituito
    da KEGG senza badare alla formattazione"""
    verbose = kwargs.get('verbose', False)
    force_download = kwargs.get('force', False)
    save = kwargs.get('force', True)

    # so you can copy paste from kegg
    args = list(chain.from_iterable(a.split('/') for a in args))
    args = [a for a in args if a]
    request = 'http://rest.kegg.jp/' + "/".join(args)
    print_verbose(verbose, "richiedo la pagina: " + request)
    filename = "./KEGG_" + "_".join(args)
    try:
        if force_download:
            raise IOError()
        print_verbose(verbose, "loading the cached file " + filename)
        with open(filename, 'r') as f:
            data = pickle.load(f)
    except IOError:
        print_verbose(verbose, "downloading the library,it may take some time")
        import urllib2
        try:
            req = urllib2.urlopen(request)
            data = req.read()
            if save:
                with open(filename, 'w') as f:
                    print_verbose(verbose, "saving the file to " + filename)
                    pickle.dump(data, f)
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


def KEGGfind(database, description, option='', **kwargs):
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

if __name__ == "__main__":
    # get the data out of a definition
    data = KEGGget('path:hsa00232')
    print data.keys()

if __name__ == "__main__":
    # lista dei pathway umani
    data_path_defs = KEGGlist('pathway', 'hsa')
    print len(data_path_defs), data_path_defs.items()[0]

if __name__ == "__main__":
    # lista dei geni umani
    data_gene_defs = KEGGlist('hsa')
    print len(data_gene_defs), data_gene_defs.items()[0]

if __name__ == "__main__":
    # lista dei compund
    data_comp_defs = KEGGlist('compound')
    print len(data_comp_defs), data_comp_defs.items()[0]

if __name__ == "__main__":
    # lista delle reazioni
    data_reac_defs = KEGGlist('reaction')
    print len(data_reac_defs), data_reac_defs.items()[0]

if __name__ == "__main__":
    # lista delle coppie di reazioni
    data_rpair_defs = KEGGlist('rpair')
    print len(data_rpair_defs), data_rpair_defs.items()[0]

if __name__ == "__main__":
    # collegamento fra pathway e geni negli umani
    data_lph, data_lhp = KEGGlink('pathway', 'hsa')
    print len(data_lph), data_lph.items()[0]
    print len(data_lhp), data_lhp.items()[0]

if __name__ == "__main__":
    # which genes are related to which reactions
    data_lrh, data_lhr = KEGGlink('reaction', 'hsa')
    print len(data_lrh), data_lrh.items()[0]
    print len(data_lhr), data_lhr.items()[0]

if __name__ == "__main__":
    # which genes are related to which compounds
    data_lch, data_lhc = KEGGlink('compound', 'hsa')
    print len(data_lch), data_lch.items()[0]
    print len(data_lhc), data_lhc.items()[0]

if __name__ == "__main__":
    # which modules are related to which pathway
    data_lmp, data_lpm = KEGGlink('module', 'hsa')
    print len(data_lmp), data_lmp.items()[0]
    print len(data_lpm), data_lpm.items()[0]

if __name__ == "__main__":
    # which genes are related to which reactions
    data_lrp, data_lpr = KEGGlink('reaction', 'pathway')
    print len(data_lrp), data_lrp.items()[0]
    print len(data_lpr), data_lpr.items()[0]
