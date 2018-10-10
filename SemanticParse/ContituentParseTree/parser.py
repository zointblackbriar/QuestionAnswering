from nltk.parse.stanford import StanfordParser, GenericStanfordParser
from nltk.internals import find_jars_within_path
from nltk.tree import Tree
from pycorenlp import StanfordCoreNLP
#The above mentioned library is to use for nltk-os comm. java library
import logging
logger = logging.getLogger(__name__)


class Parser:

    def __init__(self):
        pass

    def parse(self, sent):
        pass

class TreeLibParser(Parser):
    def __init__(self):
        self.parser = StanfordParser()

    def parse(self, line):
        """Tree objects from a sentence"""
        tree = list(self.parser.raw_parse(line))[0]
        logger.info("The results of the tree from a sentence %s", str(tree))
        tree = tree[0]
        return tree


class StanfordLibParser(TreeLibParser):
    def __init__(self):
        self.parser = StanfordParser(
            model_path= 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
        stanford_dir = self.parser._classpath.rpartition('/')[0]
        logger("stanford directory is here: %s", str(stanford_dir))
        self.parser._classpath = tuple(find_jars_within_path(stanford_dir))

class StanfordServerConnection(Parser, GenericStanfordParser):
    def __init__(self, host="http://localhost", port=9000):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=3000) # quiet = False, logging_level = logging.DEBUG

        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage' : 'en',
            'outputFormat' : 'json'
        }

    def treeConstruct(self, result):
        return Tree.fromstring(result)

    def parse(self, sent):
        output = self.nlp.annotate(sent, properties=self.props)

        if isinstance(output, str):
            return Tree('', [])

        parse_output = output['sentences'][0]['parser'] + '\n\n'
        logger.info("Output of parsing: %s", parse_output)
        tree = next(next(self._parse_trees_output(parse_output)))