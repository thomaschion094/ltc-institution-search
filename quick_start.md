# 長照機構查詢系統 - 快速開始指南

## 🚀 快速啟動

### 方法一：一鍵啟動（推薦）
```bash
bash start.sh
```

### 方法二：手動啟動
```bash
# 安裝套件
python3 -m pip install --user flask flask-cors pandas requests

# 啟動系統
python3 app.py
```

### 方法三：測試功能
```bash
# 測試基本功能（不啟動 web 服務）
python3 demo.py

# 測試縣市對照表
python3 city_mapping.py
```

## 📋 系統功能

### ✅ 已實現功能
- 🏥 **機構搜尋**: 根據縣市、鄉鎮區、服務類型篩選
- 📊 **即時資料**: 自動從衛福部下載最新 CSV 資料
- 🗺️ **地圖整合**: 點擊可開啟 Google Maps
- 📱 **響應式設計**: 支援手機和電腦
- 🔄 **資料更新**: 可手動重新載入資料
- 📞 **聯絡資訊**: 顯示電話、email、負責人

### 🎯 搜尋條件
- **縣市選擇**: 支援全台 22 縣市
- **鄉鎮區選擇**: 動態載入對應區域
- **服務類型**: 居家服務、喘息服務、巷弄長照站等

## 🌐 使用方式

1. **啟動系統**後，開啟瀏覽器訪問：
   ```
   http://127.0.0.1:5000
   ```

2. **選擇搜尋條件**：
   - 選擇縣市（必選）
   - 選擇鄉鎮區（可選）
   - 選擇服務類型（可選）

3. **查看結果**：
   - 機構名稱、地址、聯絡方式
   - 服務類型標籤
   - 特約期間資訊
   - 地圖位置（如有座標）

## 📁 檔案說明

```
├── app.py              # Flask 主程式
├── city_mapping.py     # 縣市區域對照表
├── templates/
│   └── index.html      # 網頁模板
├── static/js/
│   └── app.js         # 前端 JavaScript
├── start.sh           # 啟動腳本
├── demo.py            # 功能測試腳本
├── requirements.txt   # Python 套件清單
└── README.md          # 詳細說明文件
```

## 🔧 自訂設定

### 新增縣市區域
編輯 `city_mapping.py`，在 `CITY_DISTRICT_MAPPING` 中新增：
```python
"縣市代碼": {
    "name": "縣市名稱",
    "districts": {
        "區域代碼": "區域名稱",
        # ...
    }
}
```

### 修改搜尋欄位
1. 在 `templates/index.html` 修改表單
2. 在 `app.py` 的 `search_institutions()` 新增篩選邏輯

## 🐛 常見問題

### Q: 無法安裝套件？
A: 確認有 Python 3 和 pip：
```bash
python3 --version
python3 -m pip --version
```

### Q: 資料載入失敗？
A: 檢查網路連線，或點擊「更新資料」按鈕重試

### Q: 搜尋沒有結果？
A: 
- 確認縣市區域代碼正確
- 嘗試只選擇縣市，不選區域
- 檢查服務類型是否存在

### Q: 想要新增其他縣市？
A: 編輯 `city_mapping.py`，參考現有格式新增縣市區域對照

## 📊 資料來源

- **機構資料**: https://ltcpap.mohw.gov.tw/publish/abc.csv
- **更新頻率**: 衛福部不定期更新
- **資料欄位**: 機構名稱、代碼、地址、服務類型、聯絡方式等

## 🎨 技術架構

- **後端**: Python Flask + Pandas
- **前端**: HTML5 + Bootstrap 5 + 原生 JavaScript
- **資料處理**: CSV 解析 + 記憶體快取
- **UI 框架**: Bootstrap 響應式設計

## 📈 效能最佳化

- 資料載入後快取在記憶體
- 搜尋結果限制 100 筆避免卡頓
- 非同步 API 呼叫
- 前端載入指示器

---

**🎉 現在就開始使用吧！**

執行 `bash start.sh` 或 `python3 app.py`，然後在瀏覽器開啟 http://127.0.0.1:5000