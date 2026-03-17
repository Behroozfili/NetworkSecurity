import pytest
import os
import numpy as np
import pandas as pd

from networksecurity.utils.main_utils.utils import (
    write_yaml_file,
    read_yaml_file,
    save_numpy_array_data,
    load_numpy_array_data,
    save_object,
    load_object,
    read_data
)
from networksecurity.exception.exception import NetworkSecurityException


def test_yaml_operations(tmp_path):
    # Use pytest's tmp_path fixture for isolated file storage
    yaml_file = tmp_path / "test_config.yaml"
    file_path = str(yaml_file)
    
    # Content to write
    content = {
        "dataset": "network_data",
        "epochs": 10,
        "parameters": {"learning_rate": 0.01}
    }

    # Execute Write
    write_yaml_file(file_path=file_path, content=content)
    assert os.path.exists(file_path)

    # Execute Read
    loaded_content = read_yaml_file(file_path=file_path)

    # Assertions
    assert loaded_content == content
    assert loaded_content["epochs"] == 10


def test_numpy_array_operations(tmp_path):
    npy_file = tmp_path / "array_data.npy"
    file_path = str(npy_file)

    # Synthetic array
    original_array = np.array([[1.0, 2.0], [3.0, 4.0]])

    # Execute Save
    save_numpy_array_data(file_path=file_path, array=original_array)
    assert os.path.exists(file_path)

    # Execute Load
    loaded_array = load_numpy_array_data(file_path=file_path)

    # Assertions
    np.testing.assert_array_equal(loaded_array, original_array)


def test_object_operations(tmp_path):
    obj_file = tmp_path / "model.pkl"
    file_path = str(obj_file)

    # Synthetic object (dictionary acting as an object)
    original_object = {"model_name": "RandomForest", "accuracy": 0.95}

    # Execute Save
    save_object(file_path=file_path, obj=original_object)
    assert os.path.exists(file_path)

    # Execute Load
    loaded_object = load_object(file_path=file_path)

    # Assertions
    assert loaded_object == original_object


def test_read_data_operations(tmp_path):
    csv_file = tmp_path / "data.csv"
    file_path = str(csv_file)
    
    # Create test CSV
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    df.to_csv(file_path, index=False)
    
    # Execute Read
    loaded_df = read_data(file_path)
    
    # Assertions
    assert isinstance(loaded_df, pd.DataFrame)
    assert loaded_df.shape == (2, 2)
    assert list(loaded_df.columns) == ['col1', 'col2']


def test_exception_handling():
    # Attempting to load a non-existent file should raise a NetworkSecurityException
    with pytest.raises(NetworkSecurityException):
        load_object("non_existent_path/fake.pkl")
        
    with pytest.raises(NetworkSecurityException):
        load_numpy_array_data("non_existent_path/fake.npy")
