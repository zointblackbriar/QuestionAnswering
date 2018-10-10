#Reference: https://github.com/ayoungprogrammer/Lango

from nltk import Tree
import logging
logger = logging.getLogger(__name__)

class Matcher():
    def match_rules(tree, rules, functionCalls=None, allMatchedContext=False):
        """Matches a Tree Structure with the given query rules."""

        """tree (Tree): Parsed tree structure """
        """rules (dict): A dictionary of query rules"""
        """functionCalls (function): Function to call with context {set to None if you want to return context"""
        """allMatchedContext(Bool): IF True, returns all matched contexts, else returns first matched context"""

        if allMatchedContext is not None:
            pass


    def match_rules_context_multi(self, tree, rules, parent_context={}):
        """Recursively matches a Tree structure with rules and returns context"""

        """parent_context (dict) : Context of parent call"""
        all_contexts = []
        for template, match_rules in rules.items():
            context = parent_context.copy()
            if match_template(tree, template, context):
                parsed_contexts = []
                if not match_rules:
                    all_contexts += [context]
                else:
                    for key, child_rules in match_rules.items():
                        parsed_contexts.append(self.match_rules_context_multi(context[key], child_rules, context))
                    all_contexts += cross_context(parsed_contexts)
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

    # def match_template(self, tree, template, args=None):
    #     """Match string matches Tree Structure or not"""
    #     """tree (Tree): Parsed Tree structure of a sentence"""
    #     """template (str): String template to match. Example: (S (NP) ) """
    #
    #     tokens = get_tokens(template.split())
    #     cur_args = {}
    #     if match_tokens(tree, tokens, cur_args):
    #         if args is not None:
    #             for k ,v in cur_args.items():

    def get_object_lower(self, tree):
        return self.get_object(tree).lower()

    def get_objects(self, tree):
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
        return self.get_raw(tree).lower();