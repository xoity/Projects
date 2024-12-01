
from sklearn.ensemble import IsolationForest
import joblib

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.features = ['hour', 'attempts', 'duration']

    def train(self, log_data):
        df = self.prepare_data(log_data)
        self.model.fit(df[self.features])
        joblib.dump(self.model, 'anomaly_model.pkl')

    def detect_anomalies(self, new_data):
        df = self.prepare_data(new_data)
        predictions = self.model.predict(df[self.features])
        return predictions == -1  # True for anomalies