from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 全域變數存儲資料
ltc_data = None
city_district_mapping = {}

def load_city_district_mapping():
    """載入縣市鄉鎮區碼對照表"""
    try:
        # 優先使用從CSV生成的真實對照表
        import json
        import os
        if os.path.exists('real_city_mapping.json'):
            with open('real_city_mapping.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    
    try:
        # 備用：使用預設對照表
        from city_mapping import CITY_DISTRICT_MAPPING
        return CITY_DISTRICT_MAPPING
    except ImportError:
        # 最後備用：基本版本
        return {
            "63000": {"name": "臺北市", "districts": {
                "63000010": "中正區", "63000020": "大同區", "63000030": "中山區",
                "63000040": "松山區", "63000050": "大安區", "63000060": "萬華區",
                "63000070": "信義區", "63000080": "士林區", "63000090": "北投區",
                "63000100": "內湖區", "63000110": "南港區", "63000120": "文山區"
            }},
            "64000": {"name": "高雄市", "districts": {
                "64000010": "新興區", "64000020": "前金區", "64000030": "苓雅區",
                "64000040": "鹽埕區", "64000050": "三民區", "64000060": "左營區",
                "64000070": "楠梓區", "64000080": "鼓山區", "64000090": "前鎮區",
                "64000110": "小港區", "64000120": "旗津區", "64000130": "鳳山區",
                "64000140": "大寮區", "64000150": "林園區", "64000160": "仁武區",
                "64000170": "大樹區", "64000180": "大社區", "64000190": "岡山區",
                "64000200": "路竹區", "64000210": "橋頭區", "64000280": "燕巢區",
                "64000290": "阿蓮區"
            }}
        }

def download_and_process_csv():
    """下載並處理CSV資料 - 一個月只下載一次"""
    local_csv_file = 'data/abc.csv'
    local_processed_file = 'data/abc_processed.pkl'
    
    # 確保資料目錄存在
    os.makedirs('data', exist_ok=True)
    
    try:
        # 檢查本地檔案是否存在且在一個月內
        if os.path.exists(local_csv_file):
            file_time = os.path.getmtime(local_csv_file)
            current_time = datetime.now().timestamp()
            days_old = (current_time - file_time) / (24 * 3600)
            
            if days_old < 30:  # 30天內的檔案直接使用
                print(f"使用本地CSV檔案 (檔案建立於 {days_old:.1f} 天前)")
                
                # 如果有處理過的檔案，直接載入
                if os.path.exists(local_processed_file):
                    try:
                        df = pd.read_pickle(local_processed_file)
                        print(f"載入已處理的資料檔案，共 {len(df)} 筆記錄")
                        return df
                    except:
                        pass  # 如果載入失敗，重新處理CSV
                
                # 處理CSV檔案
                df = pd.read_csv(local_csv_file)
                df = df.dropna(subset=['機構名稱', '縣市', '區'])
                
                # 將縣市和區域代碼轉換為字串格式，以便與前端對照
                df['縣市'] = df['縣市'].astype(str)
                # 區域代碼去除 .0 後綴
                df['區'] = df['區'].astype(str).str.replace('.0', '', regex=False)
                
                # 儲存處理後的資料
                df.to_pickle(local_processed_file)
                print(f"CSV處理完成，共 {len(df)} 筆記錄")
                return df
            else:
                print(f"本地檔案已過期 ({days_old:.1f} 天)，重新下載...")
        
        # 下載新檔案
        print("正在下載最新的CSV資料...")
        url = "https://ltcpap.mohw.gov.tw/publish/abc.csv"
        response = requests.get(url, timeout=30)
        response.encoding = 'utf-8-sig'  # 處理BOM
        
        # 儲存到本地
        with open(local_csv_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"CSV檔案已下載並儲存到 {local_csv_file}")
        
        # 處理CSV
        df = pd.read_csv(local_csv_file)
        df = df.dropna(subset=['機構名稱', '縣市', '區'])
        
        # 將縣市和區域代碼轉換為字串格式，以便與前端對照
        df['縣市'] = df['縣市'].astype(str)
        # 區域代碼去除 .0 後綴
        df['區'] = df['區'].astype(str).str.replace('.0', '', regex=False)
        
        # 儲存處理後的資料
        df.to_pickle(local_processed_file)
        print(f"資料處理完成，共 {len(df)} 筆記錄")
        
        return df
        
    except Exception as e:
        print(f"處理CSV時發生錯誤: {e}")
        
        # 如果下載失敗，嘗試使用舊的本地檔案
        if os.path.exists(local_csv_file):
            print("下載失敗，使用現有的本地檔案...")
            try:
                if os.path.exists(local_processed_file):
                    df = pd.read_pickle(local_processed_file)
                else:
                    df = pd.read_csv(local_csv_file)
                    df = df.dropna(subset=['機構名稱', '縣市', '區'])
                print(f"使用本地備份檔案，共 {len(df)} 筆記錄")
                return df
            except Exception as e2:
                print(f"載入本地檔案也失敗: {e2}")
        
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cities')
def get_cities():
    """取得所有縣市列表"""
    global city_district_mapping
    if not city_district_mapping:
        city_district_mapping = load_city_district_mapping()
    
    cities = [{"code": code, "name": data["name"]} 
              for code, data in city_district_mapping.items()]
    return jsonify(cities)

@app.route('/api/districts/<city_code>')
def get_districts(city_code):
    """根據縣市代碼取得區域列表"""
    global city_district_mapping
    if not city_district_mapping:
        city_district_mapping = load_city_district_mapping()
    
    if city_code in city_district_mapping:
        districts = [{"code": code, "name": name} 
                    for code, name in city_district_mapping[city_code]["districts"].items()]
        return jsonify(districts)
    return jsonify([])

@app.route('/api/institutions')
def search_institutions():
    """搜尋機構"""
    global ltc_data, city_district_mapping
    
    # 如果資料尚未載入，先載入
    if ltc_data is None:
        ltc_data = download_and_process_csv()
        if ltc_data is None:
            return jsonify({"error": "無法載入資料"}), 500
    
    # 確保對照表已載入
    if not city_district_mapping:
        city_district_mapping = load_city_district_mapping()
    
    city_code = request.args.get('city')
    district_code = request.args.get('district')
    service_type = request.args.get('service_type', '')
    
    # 篩選資料
    filtered_data = ltc_data.copy()
    
    # 縣市篩選（如果有選擇縣市）
    if city_code:
        filtered_data = filtered_data[filtered_data['縣市'] == city_code]
        print(f"篩選縣市 '{city_code}'，找到 {len(filtered_data)} 筆")
    
    # 鄉鎮區篩選（只有在選擇了鄉鎮區時才進行篩選）
    if district_code:
        # 改為從地址進行模糊比對
        # 先從對照表取得區域名稱
        district_name = None
        if city_code in city_district_mapping:
            districts = city_district_mapping[city_code].get('districts', {})
            district_name = districts.get(district_code)
        
        if district_name:
            # 使用區域名稱在地址中進行模糊比對
            # 支援多種可能的區域名稱格式
            search_patterns = [
                district_name,  # 完整名稱，如 "三民區"
                district_name.replace('區', '').replace('市', '').replace('鎮', '').replace('鄉', '')  # 去掉後綴，如 "三民"
            ]
            
            # 建立模糊比對條件
            mask = pd.Series([False] * len(filtered_data), index=filtered_data.index)
            for pattern in search_patterns:
                if pattern:  # 確保pattern不為空
                    pattern_mask = filtered_data['地址全址'].str.contains(pattern, na=False, regex=False)
                    mask = mask | pattern_mask
            
            filtered_data = filtered_data[mask]
            print(f"使用區域名稱 '{district_name}' 進行地址模糊比對，找到 {len(filtered_data)} 筆")
        else:
            # 如果找不到區域名稱，仍使用原始代碼比對
            filtered_data = filtered_data[filtered_data['區'] == district_code]
            print(f"使用區域代碼 '{district_code}' 進行精確比對，找到 {len(filtered_data)} 筆")
    
    # 服務類型篩選（只有在選擇了特定服務類型時才進行篩選）
    if service_type:
        filtered_data = filtered_data[filtered_data['特約服務項目'].str.contains(service_type, na=False)]
        print(f"篩選服務類型 '{service_type}'，找到 {len(filtered_data)} 筆")
    
    # 轉換為字典格式
    result = []
    for _, row in filtered_data.iterrows():
        institution = {
            'name': row['機構名稱'],
            'code': row['機構代碼'],
            'type': row['機構種類'],
            'city': row['縣市'],
            'district': row['區'],
            'address': row['地址全址'],
            'longitude': row['經度'] if pd.notna(row['經度']) else None,
            'latitude': row['緯度'] if pd.notna(row['緯度']) else None,
            'service_type': row['特約服務項目'],
            'phone': row['機構電話'],
            'email': row['電子郵件'],
            'manager': row['機構負責人姓名'],
            'contract_start': row['特約起日'],
            'contract_end': row['特約迄日']
        }
        result.append(institution)
    
    return jsonify({
        'total': len(result),
        'institutions': result[:100]  # 限制返回前100筆
    })

@app.route('/api/refresh-data')
def refresh_data():
    """強制重新下載資料"""
    global ltc_data
    
    # 刪除本地檔案以強制重新下載
    local_files = ['data/abc.csv', 'data/abc_processed.pkl']
    for file_path in local_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"已刪除 {file_path}")
    
    ltc_data = download_and_process_csv()
    if ltc_data is not None:
        file_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({
            "message": "資料強制更新成功", 
            "total_records": len(ltc_data),
            "update_time": file_time
        })
    else:
        return jsonify({"error": "資料更新失敗"}), 500

@app.route('/api/data-info')
def get_data_info():
    """取得資料檔案資訊"""
    local_csv_file = 'data/abc.csv'
    info = {
        "local_file_exists": os.path.exists(local_csv_file),
        "total_records": len(ltc_data) if ltc_data is not None else 0
    }
    
    if os.path.exists(local_csv_file):
        file_time = os.path.getmtime(local_csv_file)
        current_time = datetime.now().timestamp()
        days_old = (current_time - file_time) / (24 * 3600)
        
        info.update({
            "file_date": datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S'),
            "days_old": round(days_old, 1),
            "needs_update": days_old >= 30
        })
    
    return jsonify(info)

if __name__ == '__main__':
    # 啟動時載入資料
    print("正在載入長照機構資料...")
    ltc_data = download_and_process_csv()
    city_district_mapping = load_city_district_mapping()
    
    if ltc_data is not None:
        print(f"成功載入 {len(ltc_data)} 筆機構資料")
    else:
        print("警告: 無法載入機構資料")
    
    app.run(debug=True, host='127.0.0.1', port=5000)