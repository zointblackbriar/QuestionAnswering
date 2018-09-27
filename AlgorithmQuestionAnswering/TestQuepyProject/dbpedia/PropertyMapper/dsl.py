# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Domain specific language for DBpedia quepy.
"""

from quepy.dsl import FixedType, HasKeyword, FixedRelation, FixedDataRelation

# Setup the Keywords for this application
HasKeyword.relation = "rdfs:label"
HasKeyword.language = "en"


class IsPerson(FixedType):
    fixedtype = "foaf:Person"


class IsPlace(FixedType):
    fixedtype = "PropertyMapper:Place"


class IsCountry(FixedType):
    fixedtype = "PropertyMapper-owl:Country"


class IsPopulatedPlace(FixedType):
    fixedtype = "PropertyMapper-owl:PopulatedPlace"


class IsBand(FixedType):
    fixedtype = "PropertyMapper-owl:Band"


class IsAlbum(FixedType):
    fixedtype = "PropertyMapper-owl:Album"


class IsTvShow(FixedType):
    fixedtype = "PropertyMapper-owl:TelevisionShow"


class IsMovie(FixedType):
    fixedtype = "PropertyMapper-owl:Film"


class HasShowName(FixedDataRelation):
    relation = "dbpprop:showName"
    language = "en"


class HasName(FixedDataRelation):
    relation = "dbpprop:name"
    language = "en"


class DefinitionOf(FixedRelation):
    relation = "rdfs:comment"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True


class UTCof(FixedRelation):
    relation = "dbpprop:utcOffset"
    reverse = True


class PresidentOf(FixedRelation):
    relation = "dbpprop:leaderTitle"
    reverse = True


class IncumbentOf(FixedRelation):
    relation = "dbpprop:incumbent"
    reverse = True


class CapitalOf(FixedRelation):
    relation = "PropertyMapper-owl:capital"
    reverse = True


class LanguageOf(FixedRelation):
    relation = "dbpprop:officialLanguages"
    reverse = True


class PopulationOf(FixedRelation):
    relation = "dbpprop:populationCensus"
    reverse = True


class IsMemberOf(FixedRelation):
    relation = "PropertyMapper-owl:bandMember"
    reverse = True


class ActiveYears(FixedRelation):
    relation = "dbpprop:yearsActive"
    reverse = True


class MusicGenreOf(FixedRelation):
    relation = "PropertyMapper-owl:genre"
    reverse = True


class ProducedBy(FixedRelation):
    relation = "PropertyMapper-owl:producer"


class BirthDateOf(FixedRelation):
    relation = "dbpprop:birthDate"
    reverse = True


class BirthPlaceOf(FixedRelation):
    relation = "PropertyMapper-owl:birthPlace"
    reverse = True


class ReleaseDateOf(FixedRelation):
    relation = "PropertyMapper-owl:releaseDate"
    reverse = True


class StarsIn(FixedRelation):
    relation = "dbpprop:starring"
    reverse = True


class NumberOfEpisodesIn(FixedRelation):
    relation = "PropertyMapper-owl:numberOfEpisodes"
    reverse = True


class ShowNameOf(FixedRelation):
    relation = "dbpprop:showName"
    reverse = True


class HasActor(FixedRelation):
    relation = "dbpprop:starring"


class CreatorOf(FixedRelation):
    relation = "dbpprop:creator"
    reverse = True


class NameOf(FixedRelation):
    relation = "foaf:name"
    # relation = "dbpprop:name"
    reverse = True


class DirectedBy(FixedRelation):
    relation = "PropertyMapper-owl:director"


class DirectorOf(FixedRelation):
    relation = "PropertyMapper-owl:director"
    reverse = True


class DurationOf(FixedRelation):
    # DBpedia throws an error if the relation it's
    # PropertyMapper-owl:Work/runtime so we expand the prefix
    # by giving the whole URL.
    relation = "<http://PropertyMapper.org/ontology/Work/runtime>"
    reverse = True


class HasAuthor(FixedRelation):
    relation = "PropertyMapper-owl:author"


class AuthorOf(FixedRelation):
    relation = "PropertyMapper-owl:author"
    reverse = True


class IsBook(FixedType):
    fixedtype = "PropertyMapper-owl:Book"


class LocationOf(FixedRelation):
    relation = "PropertyMapper-owl:location"
    reverse = True
