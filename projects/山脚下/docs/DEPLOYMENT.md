# 部署指南

## 环境要求

- Python 3.8+
- PostgreSQL (可选)
- 依赖包见requirements.txt

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/laobai6630-dotcom/cto.git
cd shanjiaxia_project
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置文件
```bash
cp config/config.json.example config/config.json
# 编辑config.json填入必要配置
```

4. 启动服务
```bash
python scripts/data_collection/scheduler_main.py
```

## GitHub Actions配置

配置自托管Runner以在本地服务器上运行工作流
