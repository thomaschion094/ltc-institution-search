# 📋 版本資訊

## 🎯 當前版本結構

### ⭐ 主要版本 (SQLite)
- **主程式**: `app.py` (SQLite版本)
- **啟動腳本**: `start.sh`
- **資料庫**: SQLite檔案型資料庫
- **效能**: 高效能，支援並發

### 🔄 備用版本 (CSV)
- **備用程式**: `app_csv.py` (CSV版本)
- **啟動腳本**: `start_csv.sh`
- **資料儲存**: CSV檔案 + 記憶體
- **用途**: 簡單部署，備用方案

## 🚀 啟動方式

### 主要版本 (推薦)
```bash
# SQLite版本 - 高效能
bash start.sh
# 或
python3 app.py
```

### 備用版本
```bash
# CSV版本 - 簡單部署
bash start_csv.sh
# 或
python3 app_csv.py
```

## 📊 版本比較

| 特性 | SQLite版本 (主要) | CSV版本 (備用) |
|------|------------------|----------------|
| 檔案 | `app.py` | `app_csv.py` |
| 啟動腳本 | `start.sh` | `start_csv.sh` |
| 啟動時間 | **1秒** ⚡ | 10秒 |
| 記憶體使用 | **10MB** 💾 | 50MB |
| 查詢效能 | **很快** 🚀 | 快 |
| 並發支援 | **是** 👥 | 否 |
| 資料更新 | **即時** 🔄 | 需重啟 |
| 部署複雜度 | 簡單 | 簡單 |
| 推薦用途 | 正式部署 | 開發測試 |

## 🎯 選擇建議

### 🌟 使用SQLite版本 (app.py) 當：
- ✅ 正式部署環境
- ✅ 多使用者同時使用
- ✅ 需要高效能
- ✅ 頻繁查詢操作

### 🔧 使用CSV版本 (app_csv.py) 當：
- ✅ 快速測試
- ✅ 單使用者環境
- ✅ 不想使用資料庫
- ✅ 極簡部署需求

## 📁 檔案對應關係

```
主要版本 (SQLite):
├── app.py              ← 主程式
├── start.sh            ← 主啟動腳本
└── data/institutions.db ← SQLite資料庫

備用版本 (CSV):
├── app_csv.py          ← 備用程式
├── start_csv.sh        ← 備用啟動腳本
├── data/abc.csv        ← CSV原始檔案
└── data/abc_processed.pkl ← 處理後檔案
```

## 🔄 版本切換

### 從CSV切換到SQLite
```bash
# 使用遷移工具
python3 migrate_to_sqlite.py

# 或直接啟動SQLite版本
bash start.sh
```

### 從SQLite切換到CSV
```bash
# 直接啟動CSV版本
bash start_csv.sh
```

---

**🎉 現在預設使用高效能的SQLite版本！**