
```python
import pytest
from src import utils
import os

def test_train_and_save_creates_model_and_metrics(tmp_path, monkeypatch):
    # redirect model & report directories to tmp_path
    utils.MODEL_DIR = tmp_path / "model"
    utils.REPORTS_DIR = tmp_path / "reports"
    utils.MODEL_DIR.mkdir(exist_ok=True)
    utils.REPORTS_DIR.mkdir(exist_ok=True)

    res = utils.train_and_save(default_model_name="temp_model.pkl", overwrite=True)
    assert "model_path" in res
    assert (utils.MODEL_DIR / "temp_model.pkl").exists()
    assert (utils.REPORTS_DIR / "metrics.json").exists()

def test_predict_requires_model(tmp_path):
    utils.MODEL_DIR = tmp_path / "model"
    # ensure no model present
    if utils.MODEL_DIR.exists():
        for f in utils.MODEL_DIR.iterdir():
            f.unlink()
    with pytest.raises(FileNotFoundError):
        utils.predict({"age": 30})