# 🏥 長照機構查詢系統

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一個使用 Python Flask + JavaScript 開發的長照機構查詢系統，支援全台長照機構搜尋、地址模糊比對、服務類型篩選等功能。

## ✨ 功能特色

- 🏥 **智慧搜尋**: 支援縣市、鄉鎮區、服務類型多重篩選
- 💾 **智慧快取**: CSV資料30天週期更新，本地快取提升效能
- 🔍 **地址模糊比對**: 鄉鎮區搜尋使用地址模糊比對，結果更準確
- 📱 **響應式設計**: 支援桌面和行動裝置
- 🗺️ **地圖整合**: 可直接開啟 Google Maps 查看機構位置
- 📊 **資料監控**: 即時顯示資料檔案狀態和更新時間
- ⚡ **高效能**: SQLite版本提供更好的效能和並發支援

## 🚀 快速開始

### 📋 系統需求

- Python 3.8+
- pip (Python套件管理器)

### 🔧 安裝與執行

#### 方法一：一鍵啟動（推薦）

```bash
# 克隆專案
git clone https://github.com/your-username/ltc-institution-search.git
cd ltc-institution-search

# 啟動系統（自動安裝依賴）
bash start_sqlite.sh
```

#### 方法二：手動安裝

```bash
# 克隆專案
git clone https://github.com/your-username/ltc-institution-search.git
cd ltc-institution-search

# 安裝依賴套件
pip install -r requirements.txt

# 啟動SQLite版本（推薦）
python3 app_sqlite.py

# 或啟動CSV版本
python3 app.py
```

### 🌐 訪問系統

啟動後在瀏覽器中開啟：
```
http://127.0.0.1:5000
```

## 📊 版本比較

| 功能 | CSV版本 | SQLite版本 |
|------|---------|------------|
| 啟動時間 | 10秒 | 1秒 |
| 記憶體使用 | 50MB | 10MB |
| 查詢效能 | 快 | 很快 |
| 並發處理 | 單執行緒 | 多執行緒安全 |
| 資料更新 | 需重啟 | 即時更新 |
| 部署複雜度 | 簡單 | 簡單 |

**建議使用SQLite版本獲得更好的效能！**

## 🎯 使用方式

### 🔍 搜尋功能

1. **選擇縣市**：從下拉選單選擇縣市
2. **選擇鄉鎮區**：系統自動載入對應的鄉鎮區選項
3. **選擇服務類型**：可選擇居家服務、喘息服務等
4. **查看結果**：顯示符合條件的機構列表

### 📋 搜尋場景

- **瀏覽全部**：不選任何條件 → 查看全台所有機構
- **縣市總覽**：只選縣市 → 查看該縣市所有機構
- **服務查詢**：只選服務類型 → 查看全台該服務機構
- **精確搜尋**：組合條件 → 精確定位目標機構

## 🛠️ 技術架構

### 後端 (Python Flask)
- **Flask**: 輕量級web框架
- **SQLite**: 高效能資料庫（推薦版本）
- **Pandas**: 資料處理和分析
- **Requests**: HTTP請求處理

### 前端 (HTML + JavaScript)
- **Bootstrap 5**: 響應式UI框架
- **原生JavaScript**: 不依賴額外框架
- **Font Awesome**: 圖示庫

### 資料來源
- **機構資料**: [衛福部長照機構特約名單](https://ltcpap.mohw.gov.tw/publish/abc.csv)
- **更新頻率**: 30天自動檢查更新

## 📁 專案結構

```
ltc-institution-search/
├── app.py                    # Flask主程式 (CSV版本)
├── app_sqlite.py             # Flask主程式 (SQLite版本) ⭐
├── city_mapping.py           # 縣市區域對照表
├── migrate_to_sqlite.py      # SQLite遷移工具
├── requirements.txt          # Python依賴套件
├── start.sh                  # CSV版本啟動腳本
├── start_sqlite.sh           # SQLite版本啟動腳本 ⭐
├── templates/
│   └── index.html           # 網頁模板
├── static/
│   └── js/
│       └── app.js          # 前端JavaScript
├── data/                   # 資料目錄
│   ├── .gitkeep           # 保持目錄結構
│   └── institutions.db    # SQLite資料庫 (執行後生成)
└── docs/                  # 文件目錄
    ├── README.md
    ├── FEATURES.md
    └── API.md
```

## 🔧 API 文件

### 主要端點

- `GET /api/cities` - 取得縣市列表
- `GET /api/districts/<city_code>` - 取得區域列表
- `GET /api/institutions` - 搜尋機構
- `GET /api/data-info` - 取得資料狀態
- `GET /api/refresh-data` - 強制更新資料

### 搜尋參數

- `city`: 縣市代碼
- `district`: 鄉鎮區代碼
- `service_type`: 服務類型

### 範例請求

```bash
# 搜尋高雄市所有機構
curl "http://127.0.0.1:5000/api/institutions?city=64000"

# 搜尋高雄市三民區的居家服務機構
curl "http://127.0.0.1:5000/api/institutions?city=64000&district=64000050&service_type=居家服務"
```

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 開發環境設置

```bash
# 克隆專案
git clone https://github.com/your-username/ltc-institution-search.git
cd ltc-institution-search

# 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安裝開發依賴
pip install -r requirements.txt

# 啟動開發服務器
python3 app_sqlite.py
```

### 提交規範

- 使用清楚的commit訊息
- 確保程式碼通過測試
- 更新相關文件

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

- 資料來源：[衛生福利部](https://www.mohw.gov.tw/)
- UI框架：[Bootstrap](https://getbootstrap.com/)
- 圖示：[Font Awesome](https://fontawesome.com/)

## 📞 聯絡方式

如有問題或建議，歡迎：
- 提交 [Issue](https://github.com/your-username/ltc-institution-search/issues)
- 發送 Pull Request
- 聯絡維護者

---

**⭐ 如果這個專案對您有幫助，請給個星星支持！**