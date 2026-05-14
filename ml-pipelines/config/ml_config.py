from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


@dataclass
class MLOpsConfig:
    mlflow_tracking_uri: str = field(
        default_factory=lambda: _env("MLFLOW_TRACKING_URI", "http://localhost:5000")
    )
    experiment_name: str = field(
        default_factory=lambda: _env("MLFLOW_EXPERIMENT_NAME", "salespredict_forecast")
    )
    model_registry_name: str = "sales_forecast"
    artifacts_dir: Path = field(
        default_factory=lambda: Path(
            _env("ML_ARTIFACTS_DIR", str(Path(__file__).parent.parent / "artifacts"))
        )
    )
    random_state: int = 42


_config: MLOpsConfig | None = None


def get_config() -> MLOpsConfig:
    global _config
    if _config is None:
        _config = MLOpsConfig()
    return _config
