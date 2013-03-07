# -*- coding:utf-8 -*-
from brasil.gov.vcge import config
from plone.memoize import forever
from rdflib.namespace import Namespace

import os
import rdflib


@forever.memoize
def load_skos():
    path = os.path.dirname(__file__)
    data = open(os.path.join(path, 'data', config.DEFAULT_FILE)).read()
    termos = parse_skos(data, format=config.DEFAULT_FORMAT)
    return termos


def parse_skos(data, format='xml'):
    skos = Namespace(config.NAMESPACE)
    g = rdflib.Graph()
    result = g.parse(data=data, format=format)

    objs = [s for s in result.triples((None, skos['prefLabel'], None))]

    termos = {}
    for obj in objs:
        oId = obj[0].toPython()
        title = unicode(obj[2])
        lang = obj[2].language
        if not oId in termos:
            termos[oId] = {'title': u'', 'lang': u''}
        termos[oId]['title'] = title
        termos[oId]['lang'] = lang
    return termos
