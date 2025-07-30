#!/usr/bin/env python3
"""
系統完整性檢查腳本
檢查所有檔案、套件和功能是否正常
"""

import os
import sys
from pathlib import Path

def check_files():
    """檢查必要檔案是否存在"""
    print("=== 檢查檔案結構 ===")
    
    required_files = [
        'app.py',
        'city_mapping.py', 
        'templates/index.html',
        'static/js/app.js',
        'start.sh',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (缺失)")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_packages():
    """檢查 Python 套件"""
    print("\n=== 檢查 Python 套件 ===")
    
    required_packages = [
        'flask',
        'flask_cors', 
        'pandas',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (未安裝)")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_functionality():
    """檢查核心功能"""
    print("\n=== 檢查核心功能 ===")
    
    try:
        # 檢查 Flask app 載入
        from app import app
        print("✓ Flask 應用程式載入成功")
        
        # 檢查縣市對照表
        from city_mapping import CITY_DISTRICT_MAPPING
        print(f"✓ 縣市對照表載入成功 ({len(CITY_DISTRICT_MAPPING)} 個縣市)")
        
        # 檢查資料下載功能
        import requests
        response = requests.head("https://ltcpap.mohw.gov.tw/publish/abc.csv", timeout=5)
        if response.status_code == 200:
            print("✓ CSV 資料來源可正常訪問")
        else:
            print(f"⚠ CSV 資料來源回應異常 (狀態碼: {response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"✗ 功能檢查失敗: {e}")
        return False

def check_permissions():
    """檢查檔案權限"""
    print("\n=== 檢查檔案權限 ===")
    
    if os.access('start.sh', os.X_OK):
        print("✓ start.sh 具有執行權限")
    else:
        print("⚠ start.sh 缺少執行權限，正在修復...")
        os.chmod('start.sh', 0o755)
        print("✓ start.sh 權限已修復")
    
    return True

def main():
    """主檢查函數"""
    print("🔍 長照機構查詢系統 - 完整性檢查")
    print("=" * 50)
    
    checks = [
        ("檔案結構", check_files),
        ("Python 套件", check_packages), 
        ("核心功能", check_functionality),
        ("檔案權限", check_permissions)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"✗ {check_name} 檢查時發生錯誤: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 系統檢查完成！所有功能正常")
        print("\n📋 啟動方式:")
        print("  方法一: bash start.sh")
        print("  方法二: python3 app.py")
        print("\n🌐 啟動後請訪問: http://127.0.0.1:5000")
    else:
        print("❌ 系統檢查發現問題，請檢查上述錯誤訊息")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())