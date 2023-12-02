import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score


class MenstruationDelayModule:
    def __init__(self, data: dict[str: list[int]]):
        try:
            self.model = joblib.load('menstruation_delay_pretrained_model.joblib')
        except (FileNotFoundError, EOFError, Exception):
            df = pd.DataFrame(data)

            x = df[['cycle', 'stress']]
            y = df['delay']

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

            self.model = LinearRegression()
            self.model.fit(x_train, y_train)
            joblib.dump(self.model, 'menstruation_delay_pretrained_model.joblib')

            test_predictions = self.model.predict(x_test)
            self.accuracy = accuracy_score(y_test, test_predictions)

    def predict_delay_of_menstruation(self, test_data: dict[str, list[int]]) -> int:
        predictions = self.model.predict(test_data)
        return predictions


