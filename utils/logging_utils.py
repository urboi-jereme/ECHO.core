# logging_utils.py v1.0.0

import yaml
from datetime import datetime


def log_prediction_trial(prompt, predicted_response, actual_response, compression, score, file_path='logs/PREDICTION_TRIALS.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f) or {}

    if 'trials' not in data:
        data['trials'] = []

    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'prompt': prompt,
        'predicted': predicted_response,
        'actual': actual_response,
        'compression': compression,
        'score': score
    }

    data['trials'].append(entry)

    with open(file_path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
