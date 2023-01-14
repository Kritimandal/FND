from django.shortcuts import render
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Create your views here.
clf= joblib.load('.//FND//model.sav')
tfidf_vectorizer = joblib.load('.//FND//vectorizer.sav')
# pac = joblib.load('.//FND//model.sav')

def FND(request):
    if request.method == 'POST':
        news=request.POST['news']
        vec_news_text = tfidf_vectorizer.transform([news])
        ans=clf.predict(vec_news_text)
        if ans==0:
            ans= 'Fake'
        elif ans==1:
            ans='Real'
        return render(request, 'index.html', {'result' : ans})
        return render(request, 'index.html', {'score' : ans})
    return render(request, 'index.html')

# def Data(request):
#     news= request.GET('news')
#     nb.predict([news])
#     if pred_nbs==0:
#          pred_nbs='fake'
#          print(pred_nbs)
#     elif pred_nbs==1:
#              pred_nbs='real'
#              print(pred_nbs)
#     return render(request, 'data.html', {'data' : pred_nbs})
