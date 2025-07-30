#!/usr/bin/env python3
"""
長照機構查詢系統 - 示範腳本
測試基本功能而不啟動完整的 web 服務
"""

import requests
import json
import os
from datetime import datetime

def test_csv_download():
    """測試 CSV 資料下載功能"""
    print("=== 測試 CSV 資料下載 ===")
    
    # 檢查本地檔案
    local_file = 'data/abc.csv'
    if os.path.exists(local_file):
        file_time = os.path.getmtime(local_file)
        current_time = datetime.now().timestamp()
        days_old = (current_time - file_time) / (24 * 3600)
        
        print(f"✓ 本地檔案存在: {local_file}")
        print(f"✓ 檔案建立時間: {datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✓ 檔案年齡: {days_old:.1f} 天")
        
        if days_old < 30:
            print("✓ 檔案在有效期內，無需重新下載")
            
            # 讀取本地檔案測試
            try:
                with open(local_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                print(f"✓ 本地檔案讀取成功，共 {len(lines)} 行")
                return True
            except Exception as e:
                print(f"✗ 本地檔案讀取失敗: {e}")
        else:
            print("⚠ 檔案已過期，建議重新下載")
    
    # 測試網路下載
    try:
        url = "https://ltcpap.mohw.gov.tw/publish/abc.csv"
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8-sig'
        
        lines = response.text.split('\n')
        print(f"✓ 網路下載測試成功")
        print(f"✓ 總行數: {len(lines)}")
        print(f"✓ 標題行: {lines[0][:100]}...")
        
        # 顯示前幾筆資料
        print("\n前 3 筆機構資料:")
        for i in range(1, min(4, len(lines))):
            if lines[i].strip():
                parts = lines[i].split('","')
                if len(parts) >= 4:
                    name = parts[0].replace('"', '')
                    city = parts[3].replace('"', '')
                    district = parts[4].replace('"', '')
                    print(f"  {i}. {name} ({city} {district})")
        
        return True
    except Exception as e:
        print(f"✗ 網路下載失敗: {e}")
        return False

def show_city_mapping():
    """顯示縣市對照表範例"""
    print("\n=== 縣市區域對照表範例 ===")
    mapping = {
        "63000": {"name": "臺北市", "districts": {
            "63000010": "中正區", "63000020": "大同區", "63000030": "中山區",
            "63000040": "松山區", "63000050": "大安區"
        }},
        "64000": {"name": "高雄市", "districts": {
            "64000010": "新興區", "64000020": "前金區", "64000030": "苓雅區",
            "64000040": "鹽埕區", "64000050": "三民區"
        }}
    }
    
    for city_code, city_data in mapping.items():
        print(f"✓ {city_code}: {city_data['name']}")
        for district_code, district_name in list(city_data['districts'].items())[:3]:
            print(f"    {district_code}: {district_name}")
        if len(city_data['districts']) > 3:
            print(f"    ... 還有 {len(city_data['districts']) - 3} 個區域")

def show_system_info():
    """顯示系統資訊"""
    print("=== 系統資訊 ===")
    print(f"✓ 當前時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        import pandas as pd
        print(f"✓ Pandas 版本: {pd.__version__}")
    except ImportError:
        print("✗ Pandas 未安裝")
    
    try:
        import flask
        print(f"✓ Flask 版本: {flask.__version__}")
    except ImportError:
        print("✗ Flask 未安裝")

def main():
    """主函數"""
    print("長照機構查詢系統 - 功能測試")
    print("=" * 50)
    
    show_system_info()
    print()
    
    # 測試資料下載
    if test_csv_download():
        print("\n✓ 資料下載功能正常")
    else:
        print("\n✗ 資料下載功能異常")
    
    # 顯示對照表
    show_city_mapping()
    
    print("\n" + "=" * 50)
    print("測試完成！")
    print("\n如要啟動完整系統，請執行:")
    print("  bash start.sh")
    print("或直接執行:")
    print("  python3 app.py")

if __name__ == "__main__":
    main()