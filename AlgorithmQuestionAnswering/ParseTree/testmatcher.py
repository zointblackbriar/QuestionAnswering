from ParseTree.parser import StanfordServerParser
from ParseTree.matcher import MatcherContext

#It is more likely dependency parser
parser = StanfordServerParser()
obj = MatcherContext()

# sents = [
#     'What Heatmeter contains?'
# ]
#
# rules = {
#     '(ROOT ( SBARQ ( WHNP/WDT:wh_t ) ( NP ( NN ) ( NN:np_t ) ) ) ': {
#         'np_t': {
#             '( NN ( NN:subj-o ) ( PP ( IN:subj_in-o ) ( NP:obj-o ) ) )': {},
#             '( NN:subj-o )': {},
#         },
#         'wh_t': {
#             '( WHNP:whnp ( WDT ) ( NN:prop-o ) )': {},
#             '( WHNP/WHADVP:qtype-o )': {},
#         }
#     },
#     '( SBARQ:subj-o ))': {},
# }

sents = [
    'What is the average, minimum and maximum values for sensor1?'
]

rules = {
    '( SBARQ ( WHNP/WHADVP:wh_t ) ( SQ ( VBZ ) ( NP:np_t ) ) )': {
        'np_t': {
            '( NP ( NP  ) ( PP ( IN ) ( NP (NN:obj-o ) ) ) )': {},
            '( NP:subj-o )': {},
        },
        'wh_t': {
            '( WHNP:whnp ( WDT ) ( NN:prop-o ) )': {},
            '( WHNP/WHADVP:qtype-o )': {},
        }
    },
    '( SBARQ:subj-o )': {},
}

# rules = {'( SBARQ ( WHNP/WHADVP:wh_t ) ( SQ ( VBZ ) ( NP:np_t ) ) )'}

keys = ['subj', 'subj_in', 'obj', 'prop', 'qtype']

for sent in sents:
    tree = parser.parse(sent)
    contexts = obj.match_rules(tree, rules, allMatchedContext=True)
    for context in contexts:
        print(", ".join(['%s:%s' % (k, context.get(k)) for k in keys]))