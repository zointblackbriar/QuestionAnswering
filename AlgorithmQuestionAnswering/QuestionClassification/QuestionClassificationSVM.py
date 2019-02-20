#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""@Reference: https://github.com/5hirish/adam_qas/blob/master/qas/classifier/question_classifier.py"""

#import spacy
#import csv
import logging
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.externals import joblib
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np
from sklearn import metrics
import os


logger = logging.getLogger(__name__)

#Constants

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TRAINING_DATA = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
QUESTION_CLASSIFIER_TRAINING_DATA = "qclassifier_trainer.csv"
QUESTION_CLASSIFICATION_RAW_DATA = "qclassification_data.txt"
#generated model
QUESTION_CLASSIFICATION_MODEL = "questionclassifier.pkl"

EXAMPLE_QUESTION = [
    "What is the value of sensor1 in machine1?",
    "Give me the members of linkedfactory",
    "What does linkedfactory contains?",
    "What contains IWU?"
]

EN_MODEL_DEFAULT = "en"
EN_MODEL_SM = "en_core_web_sm"
EN_MODEL_MD = "en_core_web_md"
#EN_MODEL_LG = "en_core_web_lg"

#You can use with a model or a function

class SVMClassifier():

    def pre_process(self, dta):
        return pd.get_dummies(dta)

    def feature_engineering(self, question):
        question_class = question.pop('Class')
        question.pop('Question')
        question.pop('WH-Bigram')

        return question_class


    def transform_data_matrix(self, question_train, question_predict):

        #send into a list of oolumns
        question_train_columns = list(question_train.columns)
        print("size of dataset:", len(question_train_columns))
        question_predict_columns = list(question_predict.columns)

        #clear duplicates with set
        question_trans_columns = list(set(question_train_columns + question_predict_columns))

        logger.debug("Union Columns: {0}".format(len(question_trans_columns)))

        trans_data_train = {}

        for feature in question_trans_columns:
            if feature not in question_train:
                trans_data_train[feature] = [0 for i in range(len(question_train.index))]
            else:
                trans_data_train[feature] = list(question_train[feature])

        question_train = pd.DataFrame(trans_data_train)
        logger.info("Training data: {0}".format(question_train.shape))

        question_train = csr_matrix(question_train)
        trans_data_predict = {}

        for feature in trans_data_train:
            if feature not in question_predict:
                trans_data_predict[feature] = 0
            else:
                trans_data_predict[feature] = list(question_predict[feature])

        #put into a dataframe
        question_predict = pd.DataFrame(trans_data_predict)
        logger.info("Target data: {0}".format(question_predict.shape))
        question_predict = csr_matrix(question_predict)

        return question_train, question_predict


    def predict_question_class(self, question_model, question_predict):
        return question_model.predict(question_predict), question_model

    def load_classifier_model(self, model_type="linearSVC"):

        #training_model_path = it should be hardcoded
        training_model_path = "model/LinearSVC.pkl"

        if model_type == "linearSVC":
            return joblib.load(training_model_path)

    def get_question_predict_data(self, en_doc=None, question_test = None):

        if question_test is None:
            sentence_list = list(en_doc.sents)[0:1]

        else:
            sentence_list = question_test["Question"].tolist()

            import spacy
            en_nlp = spacy.load(EN_MODEL_MD)

        question_data_frame = []

        #get all sentences
        for sentence in sentence_list:

            wh_bi_gram = []
            root_token, wh_pos, wh_nbor_pos, wh_word = [""] * 4

            if question_test is not None:
                en_doc = en_nlp(u'' + sentence)
                sentence = list(en_doc.sents)[0]

            #scan all tokens
            for token in sentence:
                if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
                    wh_pos = token.tag_
                    wh_word = token.text
                    wh_bi_gram.append(token.text)
                    wh_bi_gram.append(str(en_doc[token.i + 1]))
                    wh_nbor_pos = en_doc[token.i + 1].tag_

                if token.dep_ == "ROOT":
                    root_token = token.tag_
            question_data_frame_obj = {'WH': wh_word, 'WH-POS': wh_pos, 'WH-NBOR-POS': wh_nbor_pos,
                                       'Root-POS': root_token}
            question_data_frame.append(question_data_frame_obj)
            logger.debug("WH : {0} | WH-POS : {1} | WH-NBOR-POS : {2} | Root-POS : {3}"
                         .format(wh_word, wh_pos, wh_nbor_pos, root_token))

            question = pd.DataFrame(question_data_frame)

            return question

    def classify_question(self, en_doc=None, question_train = None, question_test = None):
        if question_train is None:
            training_path = "data/qclassifier_trainer.csv"
            #error_bad_lines=False
            #, header = 0
            question_train = pd.read_csv(training_path, sep='|', header=0)

        question_class = self.feature_engineering(question_train)

        if question_test is None:
            question_predict = self.get_question_predict_data(en_doc = en_doc)
        else:
            question_predict = self.get_question_predict_data(question_test=question_test)

        question_train = self.pre_process(question_train)
        print("size of training question:", len(question_train))
        question_predict = self.pre_process(question_predict)

        question_train, question_predict = self.transform_data_matrix(question_train, question_predict)

        question_model = self.load_classifier_model()

        logger.info("Classifier: {0}".format(question_model))

        predicted_class, svc_model = UtilsSKLearn.support_vector_machine("LinearSVC", question_train, question_class, question_predict)

        # y_true = csr_matrix(question_class)
        # y_predict = csr_matrix(question_predict)
        #Find training error
        # print("Training error SVM: ", UtilsSKLearn.training_error(y_true, y_predict))

        if question_test is not None:
            return predicted_class, svc_model, question_class, question_train
        else:
            return predicted_class

class UtilsSKLearn():
    @staticmethod
    def naive_bayes_classifier(X_train, y, X_predict):
        gnb = GaussianNB()
        gnb.fit(X_train, y)
        prediction = gnb.predict(X_predict)
        return prediction
    @staticmethod
    def support_vector_machine(method, question_train, question_class, question_predict):
        if(method == "LinearSVC"):
            model = LinearSVC()
        elif(method == "SVCgammaAuto"):
            model = SVC(gamma='auto')
        elif(method == "RbfKernel"):
            model = SVC(kernel='rbf')
        model.fit(question_train, question_class)
        prediction = model.predict(question_predict)
        return prediction, model

    @staticmethod
    def precision(y_test, y_pred, strategy = 'weighted'):
        return metrics.precision_score(y_test, y_pred, average=strategy, labels=np.unique(y_pred))

    @staticmethod
    def recall(y_test, y_pred, strategy='weighted'):
        return metrics.recall_score(y_test, y_pred, average=strategy, labels=np.unique(y_pred))

    @staticmethod
    def f1_score(y_test, y_pred, strategy='weighted'):
        return metrics.f1_score(y_test, y_pred, average=strategy, labels=np.unique(y_pred))

    @staticmethod
    def training_error(y_test, y_pred):
        prec = UtilsSKLearn.precision(y_test, y_pred)
        rec = UtilsSKLearn.recall(y_test, y_pred)
        f1 = UtilsSKLearn.f1_score(y_test, y_pred)
        return {"precision":prec, "recall":rec, "f1-score":f1}


# if __name__ == "__main__":
#     #The following line should be under main function
#     #Otherwise there will be an error like there is no configuration under __main__
#     logging.basicConfig(level=logging.DEBUG)
#     try:
#         nlp_loader = spacy.load(EN_MODEL_MD)
#         question = 'What does linkedfactory contain?'
#         doc = nlp_loader(u'' + question)
#         svmclassifier = SVMClassifier()
#         question_class = svmclassifier.classify_question(doc)
#
#
#         logger.info("Class: {0}".format(question_class))
#         logger.info("Type of the value: {0}".format(type(question_class)))
#
#     except:
#         logger.exception("Data Trainer encountered an error. PLease fix it")
