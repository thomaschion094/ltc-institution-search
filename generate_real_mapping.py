#!/usr/bin/env python3
"""
從CSV資料中提取實際的縣市區域對照表
"""

import pandas as pd
import re
import json

def extract_district_from_address(address, city_name):
    """從地址中提取區域名稱"""
    if pd.isna(address):
        return None
    
    # 不同縣市的地址模式
    patterns = [
        rf'{city_name}(\w+區)',
        rf'{city_name}(\w+市)',
        rf'{city_name}(\w+鎮)',
        rf'{city_name}(\w+鄉)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, str(address))
        if match:
            return match.group(1)
    return None

def generate_real_mapping():
    """生成實際的縣市區域對照表"""
    
    # 讀取CSV資料
    df = pd.read_csv('data/abc.csv')
    df['縣市'] = df['縣市'].astype(str)
    df['區'] = df['區'].astype(str).str.replace('.0', '', regex=False)
    
    # 縣市名稱對照
    city_names = {
        '63000': '臺北市',
        '64000': '高雄市', 
        '65000': '新北市',
        '66000': '桃園市',
        '67000': '臺中市',
        '68000': '臺南市',
        '10002': '宜蘭縣',
        '10004': '新竹縣',
        '10005': '苗栗縣',
        '10007': '彰化縣',
        '10008': '南投縣',
        '10009': '雲林縣',
        '10010': '嘉義縣',
        '10013': '屏東縣',
        '10014': '臺東縣',
        '10015': '花蓮縣',
        '10016': '澎湖縣',
        '10017': '基隆市',
        '10018': '新竹市',
        '10020': '嘉義市',
        '9007': '連江縣',
        '9020': '金門縣'
    }
    
    real_mapping = {}
    
    for city_code, city_name in city_names.items():
        if city_code not in df['縣市'].values:
            continue
            
        city_data = df[df['縣市'] == city_code].copy()
        
        # 提取區域名稱
        city_data['地址區域'] = city_data['地址全址'].apply(
            lambda addr: extract_district_from_address(addr, city_name)
        )
        
        # 建立區域對照
        districts = {}
        for _, row in city_data.iterrows():
            if pd.notna(row['區']) and pd.notna(row['地址區域']):
                district_code = row['區']
                district_name = row['地址區域']
                if district_code not in districts:
                    districts[district_code] = district_name
        
        if districts:
            real_mapping[city_code] = {
                'name': city_name,
                'districts': districts
            }
            
        print(f'{city_name} ({city_code}): {len(districts)} 個區域')
        for code in sorted(districts.keys())[:5]:  # 只顯示前5個
            name = districts[code]
            count = len(city_data[city_data['區'] == code])
            print(f'  {code}: {name} ({count} 筆)')
        if len(districts) > 5:
            print(f'  ... 還有 {len(districts) - 5} 個區域')
        print()
    
    return real_mapping

if __name__ == '__main__':
    print('=== 生成實際縣市區域對照表 ===')
    mapping = generate_real_mapping()
    
    # 儲存到檔案
    with open('real_city_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    
    print(f'✓ 已生成 {len(mapping)} 個縣市的區域對照表')
    print('✓ 已儲存到 real_city_mapping.json')