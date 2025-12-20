# API参考

## 核心API

### 数据采集API

```python
from scripts.data_collection.scheduler_main import DataCollectionScheduler

scheduler = DataCollectionScheduler()
scheduler.collect_daily_data()
```

### 特征提取API

```python
from scripts.feature_engineering.feature_extraction import FeatureExtractor

extractor = FeatureExtractor(time_window=20)
features = extractor.extract_all_features('000001', datetime.now())
```

### ML训练API

```python
from scripts.ml_training.model_training import ModelTrainer

trainer = ModelTrainer()
models = trainer.train_all_models()
```

### 筛选API

```python
from scripts.filtering.similarity_filter import SimilarityFilter

filter = SimilarityFilter()
results = filter.filter_with_multiple_thresholds([0.5, 0.4, 0.3])
```
