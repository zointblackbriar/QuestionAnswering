from collections import OrderedDict
import os
from ContituentParseTree.parser import StanfordServerParser
from ContituentParseTree.matcher import Matcher

parser = StanfordServerParser()
obj = Matcher()

sents = [
    'Who is Fraunhofer?',
    'What is BHKW?',
    'What Energy Data contains?'
]

rules = {
    '( SBARQ ( WHNP/WHADVP:wh_t ) ( SQ ( VBZ ) ( NP:np_t ) ) )': {
        'np_t': {
            '( NP ( NP:subj-o ) ( PP ( IN:subj_in-o ) ( NP:obj-o ) ) )': {},
            '( NP:subj-o )': {},
        },
        'wh_t': {
            '( WHNP:whnp ( WDT ) ( NN:prop-o ) )': {},
            '( WHNP/WHADVP:qtype-o )': {},
        }
    },
    '( SBARQ:subj-o )': {},
}

keys = ['subj', 'subj_in', 'obj', 'prop', 'qtype']

for sent in sents:
    tree = parser.parse(sent)
    contexts = obj.match_rules(tree, rules, allMatchedContext=True)
    for context in contexts:
        print(", ".join(['%s:%s' % (k, context.get(k)) for k in keys]))