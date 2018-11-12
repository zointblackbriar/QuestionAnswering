from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.externals import joblib
from sklearn import linear_model
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from CreateVector import WordVector

class QuestionAssigner():

    def precision(self, y_true, y_pred, strategy = 'weighted'):
        return metrics.precision_score(y_true, y_pred, average=strategy)

    def recall(self, y_true, y_pred, strategy='weighted'):
        return metrics.recall_score(y_true, y_pred, average=strategy)

    def f1_score(self, y_true, y_pred, strategy='weighted'):
        return metrics.f1_score(y_true, y_pred, average=strategy)

    def training_error(self, y_true, y_pred):
        prec = self.precision(y_true, y_pred)
        rec = self.recall(y_true, y_pred)
        f1 = self.f1_score(y_true, y_pred)
        return {"precision":prec, "recall":rec, "f1-score":f1}

    @staticmethod
    def encoderPass(question):
        categories = ['when', 'what', 'who', 'affirmation', 'unknown']
        encoder = LabelEncoder()
        encoder.fit(categories)
        clf = joblib.load('model/modelCreated.model')
        return QuestionAssigner.predictQuestion(encoder, clf, question)

    @staticmethod
    def predictQuestion(encoder, clf, question):
        predicted_cat = encoder.inverse_transform(clf.predict([WordVector.create_vector(question.lower())]))
        print("Predicted Category:", predicted_cat[0])
        return predicted_cat[0]

