import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch

from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.constant.training_pipeline import TARGET_COLUMN


@pytest.fixture
def mock_config():
    config = MagicMock(spec=DataTransformationConfig)
    config.transformed_train_file_path = "dummy_train.npy"
    config.transformed_test_file_path = "dummy_test.npy"
    config.transformed_object_file_path = "dummy_preprocessor.pkl"
    return config


@pytest.fixture
def mock_validation_artifact():
    artifact = MagicMock(spec=DataValidationArtifact)
    artifact.valid_train_file_path = "dummy_valid_train.csv"
    artifact.valid_test_file_path = "dummy_valid_test.csv"
    return artifact


@pytest.fixture
def synthetic_data():
    """Returns a synthetic dataframe with some NaN values."""
    data = {
        "feature1": [1.0, 2.0, np.nan, 4.0, 5.0],
        "feature2": [10, np.nan, 30, 40, 50],
        "feature3": [0.1, 0.2, 0.3, 0.4, 0.5],
        # Including the target column 
        TARGET_COLUMN: [1, -1, 1, 1, -1] 
    }
    return pd.DataFrame(data)


@patch("networksecurity.components.data_transformation.save_object")
@patch("networksecurity.components.data_transformation.save_numpy_array_data")
@patch("networksecurity.components.data_transformation.read_data")
def test_data_transformation_shapes_and_nans(mock_read_data, mock_save_npy, mock_save_obj, mock_validation_artifact, mock_config, synthetic_data):
    # Setup mocks
    mock_read_data.return_value = synthetic_data

    # Initialize transformer
    transformer = DataTransformation(
        data_validation_artifact=mock_validation_artifact,
        data_transformation_config=mock_config
    )

    # Execute
    artifact = transformer.initiate_data_transformation()

    # Assertions
    # 1. Check if mock saves were called correctly
    assert mock_save_npy.call_count == 2
    assert mock_save_obj.call_count == 2

    # 2. Extract the arguments saved to numpy array
    train_call_kwargs = mock_save_npy.call_args_list[0][1]
    test_call_kwargs = mock_save_npy.call_args_list[1][1]
    
    train_arr = train_call_kwargs.get('array')
    test_arr = test_call_kwargs.get('array')

    # 3. Check shapes (num input features + 1 target feature)
    # Synthetic data has 3 features + 1 target column = 4 columns
    assert train_arr.shape == (5, 4)
    assert test_arr.shape == (5, 4)

    # 4. Check for NaNs and Infs (imputation check)
    assert np.isnan(train_arr).sum() == 0
    assert np.isinf(train_arr).sum() == 0
    
    # 5. Target column replacement check (-1 should be 0)
    # The target column is the last column in the array (index 3)
    target_col = train_arr[:, 3]
    assert -1 not in target_col
    assert set(target_col).issubset({0, 1})
