#Reference: https://github.com/ayoungprogrammer/Lango

from nltk import Tree
import logging
logger = logging.getLogger(__name__)

class Matcher():
    def __init__(self):
        pass

    def match_rules(self, tree, rules, functionCalls=None, allMatchedContext=False):
        """Matches a Tree Structure with the given query rules."""

        """tree (Tree): Parsed tree structure """
        """rules (dict): A dictionary of query rules"""
        """functionCalls (function): Function to call with context {set to None if you want to return context"""
        """allMatchedContext(Bool): IF True, returns all matched contexts, else returns first matched context"""

        if allMatchedContext:
            logger.info("allMatchedContext")
            context = self.match_rules_context_multi(tree, rules)
        else:
            logger.info("allMatchedContext is None")
            context = self.match_rules_context(tree, rules)
            if not context:
                return None

        if functionCalls:
            args = functionCalls.__code__.co_varnames
            if allMatchedContext:
                res = []
                for c in context:
                    action_context = {}
                    for arg in args:
                        if arg in c:
                            action_context[arg] = c[arg]
                    res.append(functionCalls(**action_context))
                return res
            else:
                action_context = {}
                for arg in args:
                    if arg in context:
                        action_context[arg] = context[arg]
                return functionCalls(**action_context)
        else:
            return context

    def match_rules_context_multi(self, tree, rules, parent_context={}):
        """Recursively matches a Tree structure with rules and returns context"""

        """parent_context (dict) : Context of parent call"""
        all_contexts = []
        for template, match_rules in rules.items():
            context = parent_context.copy()
            if self.match_template(tree, template, context):
                parsed_contexts = []
                if not match_rules:
                    all_contexts += [context]
                else:
                    for key, child_rules in match_rules.items():
                        parsed_contexts.append(self.match_rules_context_multi(context[key], child_rules, context))
                    all_contexts += self.cross_context(parsed_contexts)
        return all_contexts

    def cross_context(self, context):
        """Cross product of all contexts"""

        if not context:
            return[]

        product = [{}]

        for contexts in context:
            temp_product  = []
            for item in contexts:
                for iteminnerloop in product:
                    copyItem = item.copy()
                    copyItem.update(iteminnerloop)
                    temp_product.append(copyItem)
            product = temp_product
        return product

    def match_template(self, tree, template, args=None):
        """Match string matches Tree Structure or not"""
        """tree (Tree): Parsed Tree structure of a sentence"""
        """template (str): String template to match. Example: (S (NP) ) """

        tokens = self.get_tokens(template.split())
        cur_args = {}
        if self.match_tokens(tree, tokens, cur_args):
            if args is not None:
                for k ,v in cur_args.items():
                    args[k] = v
            logger.debug('MATCHED : {0}'.format(template))
            return True
        else:
            return False

    def match_tokens(self, tree, tokens, args):
        """tree : Parsed tree structure"""
        """tokens: Stack of tokens"""

        arg_type_to_func = {
            'r': self.get_raw_lower,
            'R': self.get_raw,
            'o': self.get_object_lower,
            'O': self.get_object,
        }

        if len(tokens) == 0:
            return True

        if not isinstance(tree, Tree):
            return False

        root_token = tokens[0]

        # Equality
        if root_token.find('=') >= 0:
            eq_tokens = root_token.split('=')[1].lower().split('|')
            root_token = root_token.split('=')[0]
            word = self.get_raw_lower(tree)
            if word not in eq_tokens:
                return False

        # Get arg
        if root_token.find(':') >= 0:
            arg_tokens = root_token.split(':')[1].split('-')
            if len(arg_tokens) == 1:
                arg_name = arg_tokens[0]
                args[arg_name] = tree
            else:
                arg_name = arg_tokens[0]
                arg_type = arg_tokens[1]
                args[arg_name] = arg_type_to_func[arg_type](tree)
            root_token = root_token.split(':')[0]

        # Does not match wild card and label does not match
        if root_token != '.' and tree.label() not in root_token.split('/'):
            return False

        # Check end symbol
        if tokens[-1] == '$':
            if len(tree) != len(tokens[:-1]) - 1:
                return False
            else:
                tokens = tokens[:-1]

        # Check # of tokens
        if len(tree) < len(tokens) - 1:
            return False

        for i in range(len(tokens) - 1):
            if not self.match_tokens(tree[i], tokens[i + 1], args):
                return False
        return True
    def get_object_lower(self, tree):
        return self.get_object(tree).lower()

    def get_object(self, tree):
        """Get the object in the tree object"""
        """tree : parsed tree structure"""
        if isinstance(tree, Tree):
            #POS Tagger condition
            if tree.label() == 'DT' or tree.label() =='POS':
                return ''
            words = []
            for child in tree:
                words.append(self.get_object(child))
            return ''.join([_f  for _f in words if _f])
        else:
            return tree

    def get_raw(self, tree):

        if isinstance(tree, Tree):
            words = []
            for child in tree:
                words.append(self.get_raw(child))
            return ' '.join(words)
        else:
            return tree

    def get_raw_lower(self, tree):
        return self.get_raw(tree).lower()

    def get_tokens(self, tokens):
        """Recursively gets tokens from a match list

        Args:
            tokens : List of tokens ['(', 'S', '(', 'NP', ')', ')']
        Returns:
            Stack of tokens
        """
        tokens = tokens[1:-1]
        ret = []
        start = 0
        stack = 0
        for i in range(len(tokens)):
            if tokens[i] == '(':
                if stack == 0:
                    start = i
                stack += 1
            elif tokens[i] == ')':
                stack -= 1
                if stack < 0:
                    raise Exception('Bracket mismatch: ' + str(tokens))
                if stack == 0:
                    ret.append(self.get_tokens(tokens[start:i + 1]))
            else:
                if stack == 0:
                    ret.append(tokens[i])
        if stack != 0:
            raise Exception('Bracket mismatch: ' + str(tokens))
        return ret
