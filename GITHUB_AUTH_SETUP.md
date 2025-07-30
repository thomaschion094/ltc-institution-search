# 🔐 GitHub 認證設定指南

## ❌ 問題說明

錯誤訊息：`remote: Invalid username or token. Password authentication is not supported for Git operations.`

**原因**: GitHub 從 2021年8月13日起不再支援密碼認證，必須使用 Personal Access Token (PAT) 或 SSH 金鑰。

## ✅ 解決方案

### 方法一：使用 Personal Access Token (推薦)

#### 1️⃣ 建立 Personal Access Token

1. **登入 GitHub**: https://github.com
2. **進入設定**: 點擊右上角頭像 → Settings
3. **開發者設定**: 左側選單最下方 → Developer settings
4. **Personal access tokens**: 選擇 "Tokens (classic)"
5. **建立新 token**: 點擊 "Generate new token" → "Generate new token (classic)"

#### 2️⃣ 設定 Token 權限

**Token 名稱**: `ltc-institution-search-upload`

**到期時間**: 選擇適當的到期時間（建議30天或90天）

**權限範圍** (勾選以下項目):
- ✅ `repo` (完整的 repository 存取權限)
  - ✅ repo:status
  - ✅ repo_deployment
  - ✅ public_repo
  - ✅ repo:invite
  - ✅ security_events

**其他權限** (可選):
- ✅ `workflow` (如果需要 GitHub Actions)
- ✅ `write:packages` (如果需要發布套件)

#### 3️⃣ 複製並保存 Token

⚠️ **重要**: Token 只會顯示一次，請立即複製並安全保存！

格式類似: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### 4️⃣ 使用 Token 進行認證

```bash
# 方法A: 在 URL 中使用 token
git remote set-url origin https://您的token@github.com/您的用戶名/ltc-institution-search.git

# 方法B: 使用 Git 認證管理器
git config --global credential.helper store
git push  # 會提示輸入用戶名和密碼
# 用戶名: 您的GitHub用戶名
# 密碼: 您的Personal Access Token (不是GitHub密碼!)
```

### 方法二：使用 SSH 金鑰 (進階)

#### 1️⃣ 生成 SSH 金鑰

```bash
# 生成新的 SSH 金鑰
ssh-keygen -t ed25519 -C "您的郵箱@example.com"

# 如果系統不支援 ed25519，使用 RSA
ssh-keygen -t rsa -b 4096 -C "您的郵箱@example.com"

# 啟動 ssh-agent
eval "$(ssh-agent -s)"

# 添加 SSH 金鑰到 ssh-agent
ssh-add ~/.ssh/id_ed25519
```

#### 2️⃣ 添加 SSH 金鑰到 GitHub

```bash
# 複製公鑰到剪貼板
cat ~/.ssh/id_ed25519.pub
# 或在 macOS 上使用
pbcopy < ~/.ssh/id_ed25519.pub
```

1. **GitHub 設定**: Settings → SSH and GPG keys
2. **新增 SSH 金鑰**: New SSH key
3. **貼上公鑰**: 將複製的內容貼上
4. **儲存**: Add SSH key

#### 3️⃣ 測試 SSH 連線

```bash
# 測試 SSH 連線
ssh -T git@github.com

# 更改 remote URL 為 SSH 格式
git remote set-url origin git@github.com:您的用戶名/ltc-institution-search.git
```

## 🚀 修正後的上傳腳本

### 使用 Personal Access Token

```bash
#!/bin/bash

echo "🔐 GitHub 認證設定 - Personal Access Token 版本"

# 提示輸入資訊
read -p "GitHub 用戶名: " GITHUB_USERNAME
read -p "Repository 名稱 [ltc-institution-search]: " REPO_NAME
REPO_NAME=${REPO_NAME:-ltc-institution-search}
read -s -p "Personal Access Token: " GITHUB_TOKEN
echo ""

# 設定帶有 token 的 remote URL
REMOTE_URL="https://${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# 初始化並推送
git init
git add .
git commit -m "🏥 長照機構查詢系統 - 初始版本"
git remote add origin $REMOTE_URL
git branch -M main
git push -u origin main

echo "✅ 上傳完成！"
```

### 使用 SSH 金鑰

```bash
#!/bin/bash

echo "🔐 GitHub 認證設定 - SSH 金鑰版本"

# 提示輸入資訊
read -p "GitHub 用戶名: " GITHUB_USERNAME
read -p "Repository 名稱 [ltc-institution-search]: " REPO_NAME
REPO_NAME=${REPO_NAME:-ltc-institution-search}

# 設定 SSH remote URL
REMOTE_URL="git@github.com:${GITHUB_USERNAME}/${REPO_NAME}.git"

# 初始化並推送
git init
git add .
git commit -m "🏥 長照機構查詢系統 - 初始版本"
git remote add origin $REMOTE_URL
git branch -M main
git push -u origin main

echo "✅ 上傳完成！"
```

## 🔧 故障排除

### 常見問題

#### Q1: Token 無效
```bash
# 檢查 token 是否正確
curl -H "Authorization: token 您的token" https://api.github.com/user
```

#### Q2: Repository 不存在
1. 確認已在 GitHub 建立 repository
2. 確認 repository 名稱正確
3. 確認用戶名正確

#### Q3: 權限不足
- 確認 token 有 `repo` 權限
- 確認是 repository 的擁有者或協作者

### 驗證設定

```bash
# 檢查 remote URL
git remote -v

# 檢查 Git 設定
git config --list | grep credential

# 測試推送
git push --dry-run
```

## 💡 安全建議

### Token 安全
- ✅ 定期更新 token
- ✅ 使用最小權限原則
- ✅ 不要在程式碼中硬編碼 token
- ✅ 使用環境變數存儲 token

### 環境變數設定
```bash
# 設定環境變數
export GITHUB_TOKEN="您的token"

# 在腳本中使用
git remote set-url origin https://${GITHUB_TOKEN}@github.com/用戶名/repo名.git
```

---

**🎯 建議使用 Personal Access Token 方法，簡單且安全！**