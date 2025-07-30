# 📤 GitHub 上傳指南

## 🎯 上傳步驟

### 1️⃣ 準備工作

#### 安裝 Git
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git

# macOS (使用 Homebrew)
brew install git

# Windows
# 下載並安裝：https://git-scm.com/download/win
```

#### 設定 Git 使用者資訊
```bash
git config --global user.name "您的姓名"
git config --global user.email "您的郵箱"
```

### 2️⃣ 在 GitHub 建立 Repository

1. **登入 GitHub**: https://github.com
2. **建立新 Repository**:
   - 點擊右上角 "+" → "New repository"
   - Repository name: `ltc-institution-search`
   - Description: `長照機構查詢系統 - 支援全台長照機構搜尋`
   - 選擇 Public 或 Private
   - **不要**勾選 "Initialize this repository with a README"
   - 點擊 "Create repository"

### 3️⃣ 初始化本地 Git Repository

```bash
# 在專案目錄中執行
cd /path/to/your/project

# 初始化 Git repository
git init

# 添加所有檔案
git add .

# 建立第一次 commit
git commit -m "Initial commit: 長照機構查詢系統"
```

### 4️⃣ 連接到 GitHub Repository

```bash
# 添加遠端 repository (替換為您的 GitHub 用戶名)
git remote add origin https://github.com/您的用戶名/ltc-institution-search.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## 🔧 完整上傳腳本

創建一個自動化上傳腳本：

```bash
#!/bin/bash

echo "=== GitHub 上傳腳本 ==="

# 檢查是否在正確的目錄
if [ ! -f "app.py" ]; then
    echo "錯誤: 請在專案根目錄執行此腳本"
    exit 1
fi

# 檢查 Git 是否安裝
if ! command -v git &> /dev/null; then
    echo "錯誤: 請先安裝 Git"
    exit 1
fi

# 提示輸入 GitHub 資訊
read -p "請輸入您的 GitHub 用戶名: " GITHUB_USERNAME
read -p "請輸入 Repository 名稱 [ltc-institution-search]: " REPO_NAME
REPO_NAME=${REPO_NAME:-ltc-institution-search}

echo "正在準備上傳到: https://github.com/$GITHUB_USERNAME/$REPO_NAME"

# 初始化 Git (如果尚未初始化)
if [ ! -d ".git" ]; then
    echo "初始化 Git repository..."
    git init
fi

# 添加所有檔案
echo "添加檔案..."
git add .

# 建立 commit
echo "建立 commit..."
git commit -m "Initial commit: 長照機構查詢系統

功能特色:
- 🏥 智慧搜尋: 縣市、鄉鎮區、服務類型多重篩選
- 💾 智慧快取: 30天週期更新機制
- 🔍 地址模糊比對: 精確的區域搜尋
- 📱 響應式設計: 支援各種裝置
- ⚡ SQLite版本: 高效能資料庫支援
- 🗺️ 地圖整合: Google Maps 位置查看

技術棧:
- 後端: Python Flask + SQLite
- 前端: HTML5 + Bootstrap 5 + JavaScript
- 資料來源: 衛福部長照機構特約名單"

# 設定遠端 repository
echo "設定遠端 repository..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# 推送到 GitHub
echo "推送到 GitHub..."
git branch -M main
git push -u origin main

echo "✅ 上傳完成！"
echo "🌐 Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "📋 接下來您可以:"
echo "   1. 在 GitHub 上編輯 README.md"
echo "   2. 設定 GitHub Pages (如需要)"
echo "   3. 邀請協作者"
echo "   4. 設定 Issues 和 Projects"
```

## 📋 上傳前檢查清單

### ✅ 必要檔案
- [x] `.gitignore` - 忽略不需要的檔案
- [x] `README_GITHUB.md` - 專案說明文件
- [x] `LICENSE` - 授權條款
- [x] `requirements.txt` - Python 依賴套件

### ✅ 程式碼整理
- [x] 移除臨時檔案 (`tmp_rovodev_*`)
- [x] 移除敏感資訊 (如果有)
- [x] 確保程式碼可以正常執行
- [x] 添加適當的註解

### ✅ 文件準備
- [x] 更新 README 內容
- [x] 確保安裝和使用說明清楚
- [x] 添加螢幕截圖 (可選)

## 🎨 GitHub Repository 優化

### 📸 添加螢幕截圖
在 GitHub 上創建 `images/` 目錄，上傳系統截圖：
- 主頁面截圖
- 搜尋結果截圖
- 手機版截圖

### 🏷️ 設定 Topics
在 Repository 設定中添加 topics：
- `python`
- `flask`
- `sqlite`
- `healthcare`
- `taiwan`
- `long-term-care`
- `web-application`

### 📊 啟用 GitHub Pages (可選)
如果想要線上展示：
1. 進入 Repository Settings
2. 找到 Pages 設定
3. 選擇 source branch
4. 設定自訂域名 (可選)

## 🔄 後續維護

### 更新程式碼
```bash
# 修改程式碼後
git add .
git commit -m "描述您的更改"
git push
```

### 版本標籤
```bash
# 建立版本標籤
git tag -a v1.0.0 -m "第一個正式版本"
git push origin v1.0.0
```

### 分支管理
```bash
# 建立開發分支
git checkout -b develop
git push -u origin develop

# 建立功能分支
git checkout -b feature/new-feature
```

---

**🎉 準備好上傳到 GitHub 了！按照上述步驟即可成功上傳您的專案！**