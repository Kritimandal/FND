# Fake News Detection

![tests](https://github.com/Kritimandal/FND/actions/workflows/tests.yml/badge.svg)

A Django web app that classifies a news article as **Real** or **Fake** using a Multinomial Naive Bayes model trained on TF-IDF features. It was my college project for B.Sc. CSIT (Tribhuvan University).

## Features

- Web form: paste news text and get a prediction
- JSON API: `POST /api/predict/` for other apps to use
- Input validation (empty or very short text is rejected with HTTP 400)
- Model is loaded once and reused for every request
- 13 automated tests (unit, view, API and model tests) run on GitHub Actions

## Tech stack

Python 3.12, Django 5.1, scikit-learn 1.5, pandas, Jupyter, Bootstrap

## Model

| Item | Value |
|---|---|
| Dataset | Kaggle "Fake News" (20,800 labelled articles, label `1` = unreliable) |
| Features | Title + text, TF-IDF (English stop words removed, `max_df=0.75`) |
| Algorithm | Multinomial Naive Bayes |
| Test split | 25% |
| Accuracy | 85.42% on the test split |

The training notebook is in [`Fake_News_Detection/ml/FND.ipynb`](Fake_News_Detection/ml/FND.ipynb). The dataset is not stored in this repo. Download `train.csv` from Kaggle into `Fake_News_Detection/ml/` to re-train.

## Project structure

```
Fake_News_Detection/
├── Fake_News_Detection/   Django settings and root URLs
├── app_FND/
│   ├── predictor.py       loads the model and returns Real / Fake
│   ├── views.py           web page and JSON API
│   └── tests.py           automated tests
├── ml/                    trained model, vectorizer and notebooks
├── templates/             HTML page
└── static/                CSS, JS and images
```

## Run locally

```bash
git clone https://github.com/Kritimandal/FND.git
cd FND
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd Fake_News_Detection
python manage.py runserver
```

Open http://127.0.0.1:8000

## API

```bash
curl -X POST http://127.0.0.1:8000/api/predict/ -d "news=The Federal Reserve kept interest rates unchanged on Wednesday."
```

```json
{"result": "Real"}
```

| Status | When |
|---|---|
| 200 | Prediction returned |
| 400 | `news` is missing or shorter than 20 characters |
| 405 | Method other than POST |

## Run tests

```bash
cd Fake_News_Detection
python manage.py test
```

## Configuration

| Variable | Default | Use |
|---|---|---|
| `DJANGO_SECRET_KEY` | dev-only value | Set a real secret in production |
| `DJANGO_DEBUG` | `true` | Set `false` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host names |

## Limitations

The dataset is from 2016–2017 US news, so the model works best on English political news of that time and is less reliable on recent or Nepali news.
