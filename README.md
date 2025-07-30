# 長照機構查詢系統

這是一個使用 Python Flask 後端和 JavaScript 前端開發的長照機構查詢系統，可以根據縣市、鄉鎮區和服務類型來搜尋長照機構。

## 功能特色

- 🏥 **機構搜尋**: 根據縣市、鄉鎮區、服務類型篩選機構
- 💾 **智慧快取**: CSV資料一個月只下載一次，其他時候使用本地檔案
- 📊 **資料狀態**: 顯示本地檔案年齡和更新狀態
- 📱 **響應式設計**: 支援桌面和行動裝置
- 🗺️ **地圖整合**: 可直接開啟 Google Maps 查看機構位置
- 📞 **聯絡資訊**: 顯示機構電話、電子郵件等聯絡方式

## 系統架構

### 後端 (Python Flask)
- **app.py**: 主要應用程式，提供 REST API
- **資料處理**: 智慧快取機制，30天內使用本地檔案
- **API 端點**:
  - `/api/cities`: 取得縣市列表
  - `/api/districts/<city_code>`: 取得區域列表
  - `/api/institutions`: 搜尋機構
  - `/api/data-info`: 取得資料檔案狀態
  - `/api/refresh-data`: 強制重新下載資料

### 前端 (HTML + JavaScript)
- **Bootstrap 5**: 響應式 UI 框架
- **原生 JavaScript**: 不依賴額外框架
- **Font Awesome**: 圖示庫

## 安裝與執行

### 1. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 2. 執行應用程式
```bash
python app.py
```

### 3. 開啟瀏覽器
訪問 `http://localhost:5000`

## 資料來源

- **機構資料**: https://ltcpap.mohw.gov.tw/publish/abc.csv
- **縣市區域對照**: 內建台灣縣市區域代碼對照表

## 檔案結構

```
├── app.py                 # Flask 主應用程式
├── city_mapping.py        # 縣市區域對照表
├── requirements.txt       # Python 相依套件
├── README.md             # 說明文件
├── data/                 # 資料目錄
│   ├── abc.csv           # 下載的CSV檔案
│   └── abc_processed.pkl # 處理後的資料檔案
├── templates/
│   └── index.html        # 主頁面模板
└── static/
    └── js/
        └── app.js        # 前端 JavaScript
```

## API 說明

### 取得縣市列表
```
GET /api/cities
```

### 取得區域列表
```
GET /api/districts/{city_code}
```

### 搜尋機構
```
GET /api/institutions?city={city_code}&district={district_code}&service_type={service}
```

### 更新資料
```
GET /api/refresh-data
```

## 自訂設定

### 新增縣市區域對照
在 `app.py` 的 `load_city_district_mapping()` 函數中新增縣市區域對照：

```python
mapping = {
    "縣市代碼": {
        "name": "縣市名稱", 
        "districts": {
            "區域代碼": "區域名稱",
            # ...
        }
    },
    # ...
}
```

### 修改搜尋欄位
在 `templates/index.html` 中修改搜尋表單，並在 `app.py` 的 `search_institutions()` 函數中新增對應的篩選邏輯。

## 資料管理

### 智慧快取機制
- **自動管理**: 系統會檢查本地檔案年齡，30天內直接使用本地檔案
- **效能最佳化**: 處理後的資料以 pickle 格式儲存，載入速度更快
- **容錯機制**: 網路下載失敗時自動使用現有本地檔案
- **手動更新**: 可透過「強制更新」按鈕立即下載最新資料

### 資料狀態監控
- **檔案資訊**: 顯示本地檔案建立時間和年齡
- **更新提醒**: 超過30天會提示需要更新
- **記錄統計**: 顯示目前載入的機構數量

## 技術特點

- **前後端分離**: REST API 設計，前後端獨立開發
- **資料快取**: 機構資料載入後快取在記憶體中
- **錯誤處理**: 完整的錯誤處理和使用者提示
- **響應式設計**: 適配各種螢幕尺寸
- **效能最佳化**: 搜尋結果限制筆數，避免頁面卡頓