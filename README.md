keggrest
========

implementation of the rest API to access the kegg database

Implemented functions
--------

RESTrequest(*args, **kwargs) -> response string

    create a request to the KEGG url, is the basis for all the other call.
    Take as argument the pieces of the rest call.

KEGGlink(db1, db2, **kwargs) -> (dict, dict)

    evaluate the connection between two databases, return two dictionaries
    of list that gives how each element of the database is related to the
    elements of the other

KEGGconv(db1, db2, **kwargs) -> (dict, dict)

    convert between one kegg database and an external one. currently supported
    are the uniprot, ncbi-gi and ncbi-geneid for genes and pubchem, chebi
    for chemical compounds. Return the two lookup table (dicts) two convert
    from one dictionary to the other

KEGGlist(db, organism='', **kwargs) -> dict

    return all the element of a specific database for a certain organism,
    in the form of a dictionary element: description

KEGGget(element, option='', **kwargs) -> dict

    return the dictionary of description of the required object.
    possible options are: aaseq | ntseq | mol | kcf | image | kgml

KEGGbrite(britename, option='', **kwargs) -> dict of dicts

    analize a brite ontology and return a dictionary of dictionaries.
    still in beta version, works up to three level of hierarchy.