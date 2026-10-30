from functools import lru_cache

import joblib
from django.conf import settings

LABELS = {0: 'Real', 1: 'Fake'}


@lru_cache(maxsize=1)
def load_model():
    model = joblib.load(settings.ML_DIR / 'model.sav')
    vectorizer = joblib.load(settings.ML_DIR / 'vectorizer.sav')
    return model, vectorizer


def predict(text):
    model, vectorizer = load_model()
    label = int(model.predict(vectorizer.transform([text]))[0])
    return LABELS[label]
