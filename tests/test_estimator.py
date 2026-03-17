import pytest
import numpy as np
from unittest.mock import MagicMock

from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.exception.exception import NetworkSecurityException


@pytest.fixture
def mock_preprocessor():
    preprocessor = MagicMock()
    # Mocking standard scaler behavior: output shape equals input shape
    preprocessor.transform.side_effect = lambda x: x * 0.5 
    return preprocessor


@pytest.fixture
def mock_classifier():
    model = MagicMock()
    # Mocking a model predict: taking N samples of D dimensions, returning N predictions
    model.predict.side_effect = lambda x: np.array([1 if val[0] > 0 else 0 for val in x])
    return model


def test_estimator_forward_pass_shapes(mock_preprocessor, mock_classifier):
    # Setup
    network_model = NetworkModel(preprocessor=mock_preprocessor, model=mock_classifier)
    
    # Create input shape (N=10, D=5)
    input_shape = (10, 5)
    X_input = np.random.randn(*input_shape)

    # Execute
    predictions = network_model.prediction(X_input)

    # Assertions
    # 1. Preprocessor transform should be called once with X_input
    mock_preprocessor.transform.assert_called_once()
    
    # 2. Predict should be called once with the transformed input
    mock_classifier.predict.assert_called_once()

    # 3. Output dimension check (Predict returns N samples)
    assert predictions.shape == (10,)
    assert set(predictions).issubset({0, 1})


def test_estimator_raises_exception_on_failure(mock_preprocessor, mock_classifier):
    # Setup preprocessor to fail
    mock_preprocessor.transform.side_effect = Exception("Transformation failed due to dimension mismatch")
    network_model = NetworkModel(preprocessor=mock_preprocessor, model=mock_classifier)
    
    X_input = np.random.randn(10, 5)

    # Execute and Assert
    with pytest.raises(NetworkSecurityException) as exc_info:
        network_model.prediction(X_input)
    
    # Ensure our custom exception wraps the original error properly
    assert "Transformation failed" in str(exc_info.value)
