from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse

from .predictor import LABELS, predict
from .views import MIN_LENGTH, clean_news

REAL_NEWS = (
    'WASHINGTON (Reuters) - The U.S. Senate on Tuesday passed a bill to fund '
    'the government through December, lawmakers said.'
)
FAKE_NEWS = (
    'BREAKING: Hillary Clinton secretly arrested by FBI, mainstream media '
    'hiding the truth! Share before they delete this!'
)


class CleanNewsTests(SimpleTestCase):
    def test_strips_whitespace(self):
        news, error = clean_news('   ' + REAL_NEWS + '\n')
        self.assertEqual(news, REAL_NEWS)
        self.assertIsNone(error)

    def test_rejects_missing_text(self):
        news, error = clean_news(None)
        self.assertIsNone(news)
        self.assertIn(str(MIN_LENGTH), error)

    def test_rejects_short_text(self):
        news, error = clean_news('too short')
        self.assertIsNone(news)
        self.assertIsNotNone(error)


class HomePageTests(SimpleTestCase):
    def test_get_shows_form(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="news"')

    def test_put_is_not_allowed(self):
        response = self.client.put(reverse('home'))
        self.assertEqual(response.status_code, 405)

    @patch('app_FND.views.predict', return_value='Fake')
    def test_post_shows_prediction(self, mock_predict):
        response = self.client.post(reverse('home'), {'news': FAKE_NEWS})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fake')
        mock_predict.assert_called_once_with(FAKE_NEWS)

    @patch('app_FND.views.predict')
    def test_post_with_short_text_shows_error(self, mock_predict):
        response = self.client.post(reverse('home'), {'news': 'hi'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Please enter at least', status_code=400)
        mock_predict.assert_not_called()


class PredictApiTests(SimpleTestCase):
    @patch('app_FND.views.predict', return_value='Real')
    def test_returns_json_result(self, mock_predict):
        response = self.client.post(reverse('predict-api'), {'news': REAL_NEWS})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 'Real'})

    def test_returns_400_for_short_text(self):
        response = self.client.post(reverse('predict-api'), {'news': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_get_is_not_allowed(self):
        response = self.client.get(reverse('predict-api'))
        self.assertEqual(response.status_code, 405)


class ModelTests(SimpleTestCase):
    def test_labels_match_training_data(self):
        self.assertEqual(LABELS, {0: 'Real', 1: 'Fake'})

    def test_real_news_sample(self):
        self.assertEqual(predict(REAL_NEWS), 'Real')

    def test_fake_news_sample(self):
        self.assertEqual(predict(FAKE_NEWS), 'Fake')
