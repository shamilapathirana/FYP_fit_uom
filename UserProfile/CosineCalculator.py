from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class CosineSimilarity:
    @staticmethod
    def calculateCosinesimilarity(d1, d2):
        # d1_new = CosineSimilarity.lemmatize_sent(d1)
        sent = []
        lemmatizer = WordNetLemmatizer()
        for i in word_tokenize(d1):
            sent.append(lemmatizer.lemmatize(d1))
        # return ' '.join(sent)
        d1_new = ' '.join(sent)
        documents = [d1_new, d2]

        LemVectorizer = CountVectorizer()
        LemVectorizer.fit_transform(documents)

        tf_matrix = LemVectorizer.transform(documents).toarray()

        tfidfTran = TfidfTransformer()
        tfidfTran.fit(tf_matrix)

        tfidf_matrix = tfidfTran.transform(tf_matrix)

        cos_similarity_matrix = (tfidf_matrix * tfidf_matrix.T).toarray()
        return cos_similarity_matrix.item(1)
