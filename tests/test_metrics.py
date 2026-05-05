"""Tests for evaluation metrics."""

import numpy as np

from cardioretina.evaluation.metrics import compute_metrics


def test_compute_metrics_perfect():
    y_true = np.array([0, 0, 1, 1, 1])
    y_pred = np.array([0, 0, 1, 1, 1])
    y_prob = np.array([0.1, 0.2, 0.9, 0.8, 0.95])

    results = compute_metrics(y_true, y_pred, y_prob)
    assert results.accuracy == 1.0
    assert results.precision == 1.0
    assert results.recall == 1.0
    assert results.f1 == 1.0


def test_compute_metrics_mixed():
    y_true = np.array([0, 0, 1, 1, 0, 1])
    y_pred = np.array([0, 1, 1, 0, 0, 1])
    y_prob = np.array([0.2, 0.6, 0.8, 0.3, 0.1, 0.9])

    results = compute_metrics(y_true, y_pred, y_prob)
    assert 0 < results.accuracy < 1
    assert results.confusion_mat.shape == (2, 2)
    assert len(results.fpr) > 0
    assert len(results.tpr) > 0


def test_compute_metrics_summary():
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([0, 1, 1, 1])
    y_prob = np.array([0.1, 0.9, 0.6, 0.8])

    results = compute_metrics(y_true, y_pred, y_prob)
    summary = results.summary()
    assert "Accuracy" in summary
    assert "AUC-ROC" in summary
