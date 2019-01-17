from unittest import TestCase
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import spacy
from time import time
import unittest
import os
os.chdir(r'../')


from QuestionClassification import QuestionClassificationSVM
EN_MODEL_MD = "en_core_web_md"
nlp_loader = spacy.load(EN_MODEL_MD)
classification_object = QuestionClassificationSVM.SVMClassifier()


class TestClassifyQuestion(TestCase):

    classification_score = 0.60

    def test_classify_question(self):
        training_data_path = "data/qclassifier_trainer.csv"
        question = pd.read_csv(training_data_path, sep='|', header = 0)
        question_train, question_test = train_test_split(question, test_size=0.2, random_state=42)
        predicted_class, model, question_train_label ,question_train = classification_object.classify_question(
                                                                        question_train = question_train, question_test=question_test)

        scores = cross_val_score(model, question_train, question_train_label)
        start_time = time()
        end_time = time()
        print("Total prediction time: ", end_time - start_time)
        print("Accuracy: %0.2f (+/-%0.2f)" % (scores.mean(), scores.std() * 2))
        print("Standard deviation: ", scores.std())
        # print("Give me the all of members of linkedfactory?", classification_object.classify_question(doc1)[0])

    #65 True Result
    #35 False Result

    def test_question_1(self):
        doc1 = nlp_loader(u'' + "Give me the all of members of linkedfactory?")
        self.assertEqual(classification_object.classify_question(doc1)[0], 'HUM')

    def test_question_2(self):
        doc2 = nlp_loader(u'' + "What does linkedfactory contains?")
        self.assertEqual(classification_object.classify_question(doc2)[0], 'DESC')

    def test_question_3(self):
        doc3 = nlp_loader(u'' + "What contains linkedfactory?")
        self.assertEqual(classification_object.classify_question(doc3)[0], 'DESC')

    def test_question_4(self):
        doc4 = nlp_loader(u'' + "value sensor1 machine1?")
        self.assertEqual(classification_object.classify_question(doc4)[0], 'HUM')

    def test_question_5(self):
        doc5 = nlp_loader(u'' + "Could you give me the members in which one contains linkedfactory?")
        self.assertEqual(classification_object.classify_question(doc5)[0], 'ENTY')

    def test_question_6(self):
        doc6 = nlp_loader(u'' + "What is the average of sensor3 in machine3?")
        self.assertEqual(classification_object.classify_question(doc6)[0], 'DESC')

    def test_question_7(self):
        doc7 = nlp_loader(u'' + "Which one contains fofab?")

        self.assertEqual(classification_object.classify_question(doc7)[0], 'ENTY')
    def test_question_8(self):
        doc8 = nlp_loader(u'' + "Who is Barack Obama?")

        self.assertEqual(classification_object.classify_question(doc8)[0], 'HUM')
    def test_question_9(self):
        doc9 = nlp_loader(u'' + "Where is Liberia?")

        self.assertEqual(classification_object.classify_question(doc9)[0], 'LOC')
    def test_question_10(self):
        doc10 = nlp_loader(u'' + "What's the abbreviation for limited partnership?")

        # question 10 is wrong --ABBR
        self.assertEqual(classification_object.classify_question(doc10)[0], 'DESC')
    def test_question_11(self):
        # question 11 is wrong --ABBR
        doc11 = nlp_loader(u'' + "What does the 'c' stand for in the equation E=mc2?")

        self.assertEqual(classification_object.classify_question(doc11)[0], 'DESC')
    def test_question_12(self):
        doc12 = nlp_loader(u'' + "What are tannins?")

        self.assertEqual(classification_object.classify_question(doc12)[0], 'DESC')
    def test_question_13(self):
        doc13 = nlp_loader(u'' + "What are the words to the Canadian National anthem?")

        self.assertEqual(classification_object.classify_question(doc13)[0], 'DESC')
    def test_question_14(self):
        doc14 = nlp_loader(u'' + "How can you get rust stains out of clothing?")

        self.assertEqual(classification_object.classify_question(doc14)[0], 'DESC')
    def test_question_15(self):
        doc15 = nlp_loader(u'' + "What caused the Titanic to sink?")

        # question 15 is wrong -- ENTY
        self.assertEqual(classification_object.classify_question(doc15)[0], 'DESC')
    def test_question_16(self):
        doc16 = nlp_loader(u'' + "What are the names of Odin's ravens?")

        # question 16 is wrong -- DESC
        self.assertEqual(classification_object.classify_question(doc16)[0], 'ENTY')

    def test_question_17(self):
        doc17 = nlp_loader(u'' + "What part of your body contains the corpus callosum?")

        self.assertEqual(classification_object.classify_question(doc17)[0], 'ENTY')
    def test_question_18(self):
        doc18 = nlp_loader(u'' + "What colors make up a rainbow?")

        self.assertEqual(classification_object.classify_question(doc18)[0], 'ENTY')
    def test_question_19(self):
        doc19 = nlp_loader(u'' + "In what book can I find the story of Aladdin?")

        self.assertEqual(classification_object.classify_question(doc19)[0], 'ENTY')
    def test_question_20(self):
        doc20 = nlp_loader(u'' + "What currency is used in China?")

        self.assertEqual(classification_object.classify_question(doc20)[0], 'ENTY')
    def test_question_21(self):
        doc21 = nlp_loader(u'' + "What does Salk vaccine prevent?")

        self.assertEqual(classification_object.classify_question(doc21)[0], 'ENTY')
    def test_question_22(self):
        doc22 = nlp_loader(u'' + "What war involved the battle of Chapultepec?")

        self.assertEqual(classification_object.classify_question(doc22)[0], 'ENTY')
    def test_question_23(self):
        doc23 = nlp_loader(u'' + "What kind of nuts are used in marzipan?")

        self.assertEqual(classification_object.classify_question(doc23)[0], 'ENTY')
    def test_question_24(self):
        doc24 = nlp_loader(u'' + "What instrument does Max Roach play?")

        self.assertEqual(classification_object.classify_question(doc24)[0], 'ENTY')
    def test_question_25(self):
        doc25 = nlp_loader(u'' + "What's the official language of Algeria?")

        self.assertEqual(classification_object.classify_question(doc25)[0], 'ENTY')
    def test_question_26(self):
        doc26 = nlp_loader(u'' + "What letter appears on the cold-water tap in Spain?")

        self.assertEqual(classification_object.classify_question(doc26)[0], 'ENTY')
    def test_question_27(self):
        doc27 = nlp_loader(u'' + "What is the name of King Arthur's sword?")

        self.assertEqual(classification_object.classify_question(doc27)[0], 'ENTY')
    def test_question_28(self):
        doc28 = nlp_loader(u'' + "What is the fastest computer?")

        self.assertEqual(classification_object.classify_question(doc28)[0], 'ENTY')
    def test_question_29(self):
        doc29 = nlp_loader(u'' + "What religion has the most members?")

        self.assertEqual(classification_object.classify_question(doc29)[0], 'ENTY')
    def test_question_30(self):
        doc30 = nlp_loader(u'' + "What was the name of the ball game played by the Mayans?")

        self.assertEqual(classification_object.classify_question(doc30)[0], 'ENTY')
    def test_question_31(self):
        doc31 = nlp_loader(u'' + "What fuel do airplanes use?")

        self.assertEqual(classification_object.classify_question(doc31)[0], 'ENTY')
    def test_question_32(self):
        doc32 = nlp_loader(u'' + "What is the chemical symbol for nitrogen?")

        self.assertEqual(classification_object.classify_question(doc32)[0], 'ENTY')
    def test_question_33(self):
        doc33 = nlp_loader(u'' + "What is the best way to remove wallpaper?")

        self.assertEqual(classification_object.classify_question(doc33)[0], 'ENTY')
    def test_question_34(self):
        doc34 = nlp_loader(u'' + "How do you say 'Grandma' in Irish?")

        self.assertEqual(classification_object.classify_question(doc34)[0], 'ENTY')
    def test_question_35(self):
        doc35 = nlp_loader(u'' + "What was the name of Captain Bligh's ship?")

        self.assertEqual(classification_object.classify_question(doc35)[0], 'ENTY')
    def test_question_36(self):
        doc36 = nlp_loader(u'' + "What's the singular of dice?")

        self.assertEqual(classification_object.classify_question(doc36)[0], 'DESC')
    def test_question_37(self):
        doc37 = nlp_loader(u'' + "Who was Confucius?")

        self.assertEqual(classification_object.classify_question(doc37)[0], 'HUM')
    def test_question_38(self):
        doc38 = nlp_loader(u'' + "What are the major companies that are part of Dow Jones?")

        self.assertEqual(classification_object.classify_question(doc38)[0], 'HUM')

    def test_question_39(self):
        doc39 = nlp_loader(u'' + "Who was the first Russian astronaut to do a spacewalk?")
        self.assertEqual(classification_object.classify_question(doc39)[0], 'HUM')

    def test_question_40(self):
        doc40 = nlp_loader(u'' + "What was Queen Victoria's title regarding India?")
        self.assertEqual(classification_object.classify_question(doc40)[0], 'HUM')

    def test_question_41(self):
        doc41 = nlp_loader(u'' + "What' s the oldest capital city in the Americas?")
        self.assertEqual(classification_object.classify_question(doc41)[0], 'LOC')
    def test_question_42(self):
        doc42 = nlp_loader(u'' + "What is the highest peak in Africa?")
        self.assertEqual(classification_object.classify_question(doc42)[0], 'LOC')

    def test_question_43(self):
        doc43 = nlp_loader(u'' + "What river runs through Liverpool?")
        self.assertEqual(classification_object.classify_question(doc43)[0], 'LOC')
    def test_question_44(self):
        doc44 = nlp_loader(u'' + "What states do not have state income tax?")
        self.assertEqual(classification_object.classify_question(doc44)[0], 'LOC')
    def test_question_45(self):
        doc45 = nlp_loader(u'' + "What is the telephone number for the University of Colorado?")
        self.assertEqual(classification_object.classify_question(doc45)[0], 'NUM')
    def test_question_46(self):
        doc46 = nlp_loader(u'' + "About how many soldiers died in World War II?")
        self.assertEqual(classification_object.classify_question(doc46)[0], 'NUM')
    def test_question_47(self):
        doc47 = nlp_loader(u'' + "What is the date of Boxing Day?")
        self.assertEqual(classification_object.classify_question(doc47)[0], 'NUM')
    def test_question_48(self):
        doc48 = nlp_loader(u'' + "How long was Mao's 1930s Long March?")
        self.assertEqual(classification_object.classify_question(doc48)[0], 'NUM')
    def test_question_49(self):
        doc49 = nlp_loader(u'' + "How much did a McDonald's hamburger cost in 1963?")
        self.assertEqual(classification_object.classify_question(doc49)[0], 'NUM')
    def test_question_50(self):
        doc50 = nlp_loader(u'' + "What fraction of a beaver's life is spent swimming?")
        self.assertEqual(classification_object.classify_question(doc50)[0], 'NUM')
    def test_question_51(self):
        doc51 = nlp_loader(u'' + "How hot should the oven be when making Peachy Oat Muffins?")
        self.assertEqual(classification_object.classify_question(doc51)[0], 'NUM')
    def test_question_52(self):
        doc52 = nlp_loader(u'' + "How many pounds are there in a stone?")
        self.assertEqual(classification_object.classify_question(doc52)[0], 'NUM')
    def test_question_53(self):
        doc53 = nlp_loader(u'' + "How fast must a spacecraft travel to escape Earth's gravity?")
        self.assertEqual(classification_object.classify_question(doc53)[0], 'NUM')
    def test_question_54(self):
        doc54 = nlp_loader(u'' + "What is the size of Argentina?")
        self.assertEqual(classification_object.classify_question(doc54)[0], 'NUM')

    def test_question_101(self):
        doc101 = nlp_loader(u'' + "How far is it from Denver to Aspen ?")
        self.assertEqual(classification_object.classify_question(doc101)[0], 'NUM')

    def test_question_55(self):
        doc55 = nlp_loader(u'' + "What county is Modesto , California in ?")
        self.assertEqual(classification_object.classify_question(doc55)[0], 'LOC')
    def test_question_56(self):
        doc56 = nlp_loader(u'' + "Who was Galileo ?")
        self.assertEqual(classification_object.classify_question(doc56)[0], 'HUM')
    def test_question_57(self):
        doc57 = nlp_loader(u'' + "What is an atom ?")
        self.assertEqual(classification_object.classify_question(doc57)[0], 'DESC')
    def test_question_58(self):
        doc58 = nlp_loader(u'' + "When did Hawaii become a state ?")
        self.assertEqual(classification_object.classify_question(doc58)[0], 'NUM')
    def test_question_59(self):
        doc59 = nlp_loader(u'' + "How tall is the Sears Building ?")
        self.assertEqual(classification_object.classify_question(doc59)[0], 'NUM')
    def test_question_60(self):
        doc60 = nlp_loader(u'' + "George Bush purchased a small interest in which baseball team ?")
        self.assertEqual(classification_object.classify_question(doc60)[0], 'HUM')
    def test_question_61(self):
        doc61 = nlp_loader(u'' + "What is Australia 's national flower ?")
        self.assertEqual(classification_object.classify_question(doc61)[0], 'ENTY')
    def test_question_62(self):
        doc62 = nlp_loader(u'' + "Why does the moon turn orange ?")
        self.assertEqual(classification_object.classify_question(doc62)[0], 'DESC')
    def test_question_63(self):
        doc63 = nlp_loader(u'' + "What is autism ?")
        self.assertEqual(classification_object.classify_question(doc63)[0], 'DESC')
    def test_question_64(self):
        doc64 = nlp_loader(u'' + "What city had a world fair in 1900 ?")
        self.assertEqual(classification_object.classify_question(doc64)[0], 'LOC')
    def test_question_65(self):
        doc65 = nlp_loader(u'' + "What person 's head is on a dime ?")
        self.assertEqual(classification_object.classify_question(doc65)[0], 'HUM')
    def test_question_66(self):
        doc66 = nlp_loader(u'' + "What is the average weight of a Yellow Labrador ?")
        self.assertEqual(classification_object.classify_question(doc66)[0], 'NUM')
    def test_question_67(self):
        doc67 = nlp_loader(u'' + "Who was the first man to fly across the Pacific Ocean ?")
        self.assertEqual(classification_object.classify_question(doc67)[0], 'HUM')
    def test_question_68(self):
        doc68 = nlp_loader(u'' + "When did Idaho become a state ?")
        self.assertEqual(classification_object.classify_question(doc68)[0], 'NUM')
    def test_question_69(self):
        doc69 = nlp_loader(u'' + "What is the life expectancy for crickets ?")
        self.assertEqual(classification_object.classify_question(doc69)[0], 'NUM')
    def test_question_70(self):
        doc70 = nlp_loader(u'' + "What metal has the highest melting point ?")
        self.assertEqual(classification_object.classify_question(doc70)[0], 'ENTY')
    def test_question_71(self):
        doc71 = nlp_loader(u'' + "Who developed the vaccination against polio ?")
        self.assertEqual(classification_object.classify_question(doc71)[0], 'HUM')
    def test_question_72(self):
        doc72 = nlp_loader(u'' + "What is epilepsy ?")
        self.assertEqual(classification_object.classify_question(doc72)[0], 'DESC')
    def test_question_73(self):
        doc73 = nlp_loader(u'' + "What year did the Titanic sink ?")
        self.assertEqual(classification_object.classify_question(doc73)[0], 'NUM')
    def test_question_74(self):
        doc74 = nlp_loader(u'' + "Who was the first American to walk in space ?")
        self.assertEqual(classification_object.classify_question(doc74)[0], 'HUM')
    def test_question_75(self):
        doc75 = nlp_loader(u'' + "What is a biosphere ?")
        self.assertEqual(classification_object.classify_question(doc75)[0], 'DESC')
    def test_question_76(self):
        doc76 = nlp_loader(u'' + "What river in the US is known as the Big Muddy ?")
        self.assertEqual(classification_object.classify_question(doc76)[0], 'LOC')

    def test_question_77(self):
        doc77 = nlp_loader(u'' + "What is the name of the chocolate company in San Francisco ?")
        self.assertEqual(classification_object.classify_question(doc77)[0], 'HUM')

    def test_question_78(self):
        doc78 = nlp_loader(u'' + "What is bipolar disorder ?")
        self.assertEqual(classification_object.classify_question(doc78)[0], 'DESC')
    def test_question_79(self):
        doc79 = nlp_loader(u'' + "What is cholesterol ?")
        self.assertEqual(classification_object.classify_question(doc79)[0], 'DESC')
    def test_question_80(self):
        doc80 = nlp_loader(u'' + "Who developed the Macintosh computer ?")
        self.assertEqual(classification_object.classify_question(doc80)[0], 'HUM')
    def test_question_81(self):
        doc81 = nlp_loader(u'' + "What is caffeine ?")
        self.assertEqual(classification_object.classify_question(doc81)[0], 'DESC')
    def test_question_82(self):
        doc82 = nlp_loader(u'' + "What imaginary line is halfway between the North and South Poles ?")
        self.assertEqual(classification_object.classify_question(doc82)[0], 'LOC')
    def test_question_83(self):
        doc83 = nlp_loader(u'' + "Where is John Wayne airport ?")
        self.assertEqual(classification_object.classify_question(doc83)[0], 'LOC')
    def test_question_84(self):
        doc84 = nlp_loader(u'' + "What hemisphere is the Philippines in ?")
        self.assertEqual(classification_object.classify_question(doc84)[0], 'LOC')
    def test_question_85(self):
        doc85 = nlp_loader(u'' + "What is the average speed of the horses at the Kentucky Derby ?")
        self.assertEqual(classification_object.classify_question(doc85)[0], 'NUM')
    def test_question_86(self):
        doc86 = nlp_loader(u'' + "Where are the Rocky Mountains ?")
        self.assertEqual(classification_object.classify_question(doc86)[0], 'LOC')
    def test_question_87(self):
        doc87 = nlp_loader(u'' + "What are invertebrates ?")
        self.assertEqual(classification_object.classify_question(doc87)[0], 'DESC')
    def test_question_88(self):
        doc88 = nlp_loader(u'' + "What is the temperature at the center of the earth ?")
        self.assertEqual(classification_object.classify_question(doc88)[0], 'NUM')
    def test_question_89(self):
        doc89 = nlp_loader(u'' + "When did John F. Kennedy get elected as President ?")
        self.assertEqual(classification_object.classify_question(doc89)[0], 'NUM')
    def test_question_90(self):
        doc90 = nlp_loader(u'' + "How old was Elvis Presley when he died ?")
        self.assertEqual(classification_object.classify_question(doc90)[0], 'NUM')
    def test_question_91(self):
        doc91 = nlp_loader(u'' + "Where is the Orinoco River ?")
        self.assertEqual(classification_object.classify_question(doc91)[0], 'LOC')
    def test_question_92(self):
        doc92 = nlp_loader(u'' + "How far is the service line from the net in tennis ?")
        self.assertEqual(classification_object.classify_question(doc92)[0], 'NUM')
    def test_question_93(self):
        doc93 = nlp_loader(u'' + "How much fiber should you have per day ?")
        self.assertEqual(classification_object.classify_question(doc93)[0], 'NUM')
    def test_question_94(self):
        doc94 = nlp_loader(u'' + "How many Great Lakes are there ?")
        self.assertEqual(classification_object.classify_question(doc94)[0], 'NUM')
    def test_question_95(self):
        doc95 = nlp_loader(u'' + "Material called linen is made from what plant ?")
        self.assertEqual(classification_object.classify_question(doc95)[0], 'ENTY')
    def test_question_96(self):
        doc96 = nlp_loader(u'' + "What is Teflon ?")
        self.assertEqual(classification_object.classify_question(doc96)[0], 'DESC')
    def test_question_97(self):
        doc97 = nlp_loader(u'' + "What is amitriptyline ?")
        self.assertEqual(classification_object.classify_question(doc97)[0], 'DESC')
    def test_question_98(self):
        doc98 = nlp_loader(u'' + "What is amitriptyline ?")
        self.assertEqual(classification_object.classify_question(doc98)[0], 'DESC')
    def test_question_99(self):
        doc99 = nlp_loader(u'' + "What is the proper name for a female walrus ?")
        self.assertEqual(classification_object.classify_question(doc99)[0], 'ENTY')
    def test_question_100(self):
        doc100 = nlp_loader(u'' + "What is a group of turkeys called ?")
        self.assertEqual(classification_object.classify_question(doc100)[0], 'ENTY')




if __name__ == '__main__':
    unittest.main()