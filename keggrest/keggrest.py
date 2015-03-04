# -*- coding: utf-8 -*-
"""
Database           Name           Abbrev         kid     Remark
KEGG PATHWAY     pathway     path     map number
KEGG BRITE           brite     br     br number
KEGG MODULE     module     md     M number
KEGG DISEASE     disease     ds     H number     Japanese version: disease_ja ds_ja
KEGG DRUG           drug           dr     D number     Japanese version: drug_ja dr_ja
KEGG ENVIRON     environ     ev     E number     Japanese version: environ_ja ev_ja
KEGG ORTHOLOGY     orthology     ko     K number
KEGG GENOME     genome     genome     T number
KEGG GENOMES     genomes     gn     T number     Composite database: genome + egenome + mgenome
KEGG GENES           genes     -     -     Composite database: consisting of KEGG organisms
KEGG LIGAND     ligand     ligand     -     Composite database: compound + glycan + reaction + rpair + rclass + enzyme
KEGG COMPOUND     compound     cpd     C number     Japanese version: compound_ja cpd_ja
KEGG GLYCAN     glycan     gl     G number
KEGG REACTION     reaction     rn     R number
KEGG RPAIR           rpair     rp     RP number
KEGG RCLASS     rclass     rc     RC number
KEGG ENZYME     enzyme     ec     -
"""

# %%
import requests
from collections import defaultdict

# %%


def get_possible_kegg_actions():
    """return the possible rest action possible on the KEGG database
    """
    return ['info', 'list', 'find', 'get', 'conv', 'link']


def _generate_keggrest_request(*args):
    """join the pieces and generate the rest request.

    Check for correct action, raises ValueError if the action is not a
    legitimate one.

    legitimate actions:
    ['info', 'list', 'find', 'get', 'conv', 'link']
    """
    action = args[0]
    valid_actions = get_possible_kegg_actions()

    if action not in valid_actions:
        errors_str = ("the requested action `{}` "
                      "is not in the list of correct ones: {}")
        raise ValueError(errors_str.format(action, "; ".join(valid_actions)))

    return 'http://rest.kegg.jp/' + "/".join(args)


def _split_lines(data):
    """Split the lines as two tab separated entries.

    Take the raw dump from a kegg request that contains
    a list of tuples divided by tabs (the standard list format for kegg)
    and returns a list of tuples
    """
    # split the lines
    splitted_lines = data.splitlines()
    # divide the tabs
    splitted_lines = [line.split('\t') for line in splitted_lines]
    result = []
    for line in splitted_lines:
        if line and line[0].strip():
            trimmed = tuple(element.strip() for element in line)
            result.append(trimmed)
    return result


def _double_way_hashtable(list_of_couples):
    """take a list of couple and create two dictionaries from that.

    Assuming that each couple looks like (entry1, entry2)
    the first dictionary is a list ofall the entry2 linked to each entry1.
    the second one is the reciprocal of that
    """
    data = list_of_couples
    rel_dir = defaultdict(list)
    rel_inv = defaultdict(list)
    data_lines = (line for line in data if line)
    for elements in data_lines:
        if not len(elements) == 2:
            t = "the line need to have two elements to be split, received: {}"
            raise ValueError(t.format(repr(elements)))
        element_1, element_2 = elements
        rel_dir[element_1].append(element_2)
        rel_inv[element_2].append(element_1)
    return rel_dir, rel_inv

# %%


def RESTrequest(*args):
    """dumps the result from the KEGG REST API
    """
    request = _generate_keggrest_request(*args)
    # this could rise a ConnectionsError
    result = requests.get(request, timeout=None)
    # if there was a problem with the page, this would rise
    # requests.exceptions.HTTPError
    result.raise_for_status()
    return result.text

# %%


def KEGGlink(db1, db2):
    """Links the content of two different databases.

    It returns two dictionaries, giving the direct and inverse linkage
    between the two databases.

    Usage
    =======

    The function takes the name of the two databases that should be
    linked. The databases should be one of the following:
        * pathway
        * brite
        * module
        * disease
        * drug
        * environ
        * ko
        * genome
        * <org> (the organism code to be linked)
        * compound
        * glycan
        * reaction
        * rpair
        * rclass
        * enzyme
        * genes
        * pubmed

    It is possible to replace the second database with an entry from a
    different database, obtaining the list of partial relationships
    between that single element and all the elements from the other
    database

    Correspond to the following rest request::

        http://rest.kegg.jp/link/<target_db>/<source_db>

    EXAMPLES
    =========

    Getting all the E. coli genes that are related to a specific pathway::

        path2genes, genes2path = keggrest.KEGGlink('ec', 'map00010')

    Getting all the connections between human genes and pathways::

        path2genes, gene2paths = keggrest.KEGGlink('hsa', 'pathway')

    The reverse operation also works::

        gene2paths, path2genes = keggrest.KEGGlink('pathway', 'hsa')
    """

    data = RESTrequest(u'link', db1, db2)
    couples = _split_lines(data)
    return _double_way_hashtable(couples)


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
    data = _split_lines(data)
    return dict(data)


def KEGGfind(database, searchterm, **kwargs):
    """retrieve all the elements in all the databases that are
    related to the given search string

    it returns a dictionary containing the obtained entries description
    """

    data = RESTrequest(u'find', database, searchterm, **kwargs)
    data = _split_lines(data)
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
    couples = _split_lines(data)
    return _double_way_hashtable(couples)



def KEGGget(element, option=u'', parse_reference=True, **kwargs):
    """retrieve an element from a  database

    currently it doesn't work when options are used

    if parse_reference is True, it will transform the REFERENCE section
    (if present) in a dictionary indicized by the PMID code of the articles.
    This could drop few rare entries that are badly formatted.

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
    if parse_reference and 'REFERENCE' in result:
        reference_seq = result['REFERENCE']
        reference_seq = list(zip(*([iter(reference_seq)] * 4)))
        reference_seq_filtered = {}
        for reference in reference_seq:
            code = reference[0]
            if code.startswith('PMID:'):
                biblio_info = {}
                biblio_info['AUTHORS'] = reference[1]
                biblio_info['TITLE'] = reference[2]
                biblio_info['JOURNAL'] = reference[3]
                reference_seq_filtered[code] = biblio_info
        result['REFERENCE'] = reference_seq_filtered
    elif parse_reference and 'REFERENCE' not in result:
        result['REFERENCE'] = {}
    return result
