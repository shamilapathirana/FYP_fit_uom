
class AccuracyBased:

    def predict(mnb_classifier, logreg_classifier, linsvc_classifier, mnb_acc, logreg_acc, linsvc_acc, tweets_tf):
        result_array = []
        mnb_predict = mnb_classifier.predict_proba(tweets_tf)
        logreg_predict = logreg_classifier.predict_proba(tweets_tf)
        linsvc_predict = linsvc_classifier.predict_proba(tweets_tf)

        sum_acc = mnb_acc + logreg_acc + linsvc_acc

        for i in range(len(mnb_predict)):
            predict_array = []
            env = ("Environment", ((mnb_predict[i][0] * mnb_acc) + (logreg_predict[i][0] * logreg_acc) + (
                    linsvc_predict[i][0] * linsvc_acc)) / sum_acc)
            predict_array.append(env)
            fin = ("Finance", ((mnb_predict[i][1] * mnb_acc) + (logreg_predict[i][1] * logreg_acc) + (
                    linsvc_predict[i][1] * linsvc_acc)) / sum_acc)
            predict_array.append(fin)
            foo = ("Food", ((mnb_predict[i][2] * mnb_acc) + (logreg_predict[i][2] * logreg_acc) + (
                    linsvc_predict[i][2] * linsvc_acc)) / sum_acc)
            predict_array.append(foo)
            hot = ("Hotel", ((mnb_predict[i][3] * mnb_acc) + (logreg_predict[i][3] * logreg_acc) + (
                    linsvc_predict[i][3] * linsvc_acc)) / sum_acc)
            predict_array.append(hot)

            predict_array.sort(key=lambda x: x[1], reverse=True)
            if (predict_array[0][1] + predict_array[1][1]) > 0.677:
                prediction = predict_array[0][0]
            else:
                prediction = "Other"
            result_array.append(prediction)

        return result_array

