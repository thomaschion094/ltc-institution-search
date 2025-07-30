#!/bin/bash

echo "=== 長照機構查詢系統啟動腳本 (CSV版本) ==="

# 檢查 Python3 是否存在
if ! command -v python3 &> /dev/null; then
    echo "錯誤: 找不到 python3，請先安裝 Python 3"
    exit 1
fi

# 安裝相依套件
echo "正在安裝相依套件..."
python3 -m pip install --user flask flask-cors pandas requests openpyxl

# 檢查安裝是否成功
echo "檢查套件安裝..."
python3 -c "import flask, pandas, requests; print('✓ 所有套件安裝成功')" || {
    echo "錯誤: 套件安裝失敗"
    exit 1
}

# 啟動應用程式
echo "啟動長照機構查詢系統..."
echo "請在瀏覽器中開啟: http://127.0.0.1:5000"
echo "按 Ctrl+C 停止服務"
echo ""

python3 app_csv.py