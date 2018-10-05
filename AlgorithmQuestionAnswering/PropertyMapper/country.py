# coding: utf-8

from refo import Plus, Question
from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Pos, QuestionTemplate, Token, Particle
from dsl import IsCountry, IncumbentOf, CapitalOf, \
    LabelOf, LanguageOf, PopulationOf, PresidentOf


class Country(Particle):
    regex = Plus(Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS"))

    def interpret(self, match):
        name = match.words.tokens.title()
        return IsCountry() + HasKeyword(name)


class PresidentOfQuestion(QuestionTemplate):

    regex = Pos("WP") + Token("is") + Question(Pos("DT")) + \
        Lemma("president") + Pos("IN") + Country() + Question(Pos("."))

    def interpret(self, match):
        president = PresidentOf(match.country)
        incumbent = IncumbentOf(president)
        label = LabelOf(incumbent)

        return label, "enum"


class CapitalOfQuestion(QuestionTemplate):

    opening = Lemma("what") + Token("is")
    regex = opening + Pos("DT") + Lemma("capital") + Pos("IN") + \
        Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        capital = CapitalOf(match.country)
        label = LabelOf(capital)
        return label, "enum"


# FIXME: the generated query needs FILTER isLiteral() to the head
# because PropertyMapper sometimes returns different things
class LanguageOfQuestion(QuestionTemplate):

    openings = (Lemma("what") + Token("is") + Pos("DT") +
                Question(Lemma("official")) + Lemma("language")) | \
               (Lemma("what") + Lemma("language") + Token("is") +
                Lemma("speak"))

    regex = openings + Pos("IN") + Question(Pos("DT")) + Country() + \
        Question(Pos("."))

    def interpret(self, match):
        language = LanguageOf(match.country)
        return language, "enum"


class PopulationOfQuestion(QuestionTemplate):

    openings = (Pos("WP") + Token("is") + Pos("DT") +
                Lemma("population") + Pos("IN")) | \
               (Pos("WRB") + Lemma("many") + Lemma("people") +
                Token("live") + Pos("IN"))
    regex = openings + Question(Pos("DT")) + Country() + Question(Pos("."))

    def interpret(self, match):
        population = PopulationOf(match.country)
        return population, "literal"
