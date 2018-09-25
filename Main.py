import Utils, nltk

#TODO: Add init __name__
searchParam = input("Search your input:")
#searchParam = "What is Fraunhofer?"
try:
    takeWords = []
    takeWords = Utils.clearTokenAndStopWords(searchParam)
    print(takeWords)
    tagged_Words = nltk.pos_tag(takeWords)
    print(tagged_Words)
    print("Searching...")
    #Utils.taggedWhoQuestion(tagged_Words)
    #Utils.taggedWhereQuestion(tagged_Words)
    Utils.taggedWhatQuestion(tagged_Words)
except:
    print("An Exception caught")
