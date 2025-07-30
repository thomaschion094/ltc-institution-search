#!/usr/bin/env python3
"""
長照機構查詢系統 - SQLite 資料庫版本
提供更好的效能和擴展性
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
import pandas as pd
import requests
import json
from datetime import datetime
import os
import threading

app = Flask(__name__)
CORS(app)

# 資料庫設定
DATABASE_PATH = 'data/institutions.db'
city_district_mapping = {}

# 資料庫連線池 (簡單實現)
db_lock = threading.Lock()

def get_db_connection():
    """取得資料庫連線"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以像字典一樣存取
    return conn

def init_database():
    """初始化資料庫結構"""
    os.makedirs('data', exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 建立機構主表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT,
            type TEXT,
            city_code TEXT,
            district_code TEXT,
            address TEXT,
            longitude REAL,
            latitude REAL,
            o_abc TEXT,
            service_type TEXT,
            contract_city TEXT,
            contract_district TEXT,
            phone TEXT,
            email TEXT,
            manager TEXT,
            contract_start TEXT,
            contract_end TEXT,
            last_updated TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 建立索引以提升查詢效能
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_city_code ON institutions(city_code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_district_code ON institutions(district_code)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_address ON institutions(address)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_service_type ON institutions(service_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON institutions(name)')
    
    conn.commit()
    conn.close()
    print("✓ 資料庫初始化完成")

def load_city_district_mapping():
    """載入縣市鄉鎮區碼對照表"""
    global city_district_mapping
    try:
        # 優先使用從CSV生成的真實對照表
        if os.path.exists('real_city_mapping.json'):
            with open('real_city_mapping.json', 'r', encoding='utf-8') as f:
                city_district_mapping = json.load(f)
                return
    except:
        pass
    
    try:
        # 備用：使用預設對照表
        from city_mapping import CITY_DISTRICT_MAPPING
        city_district_mapping = CITY_DISTRICT_MAPPING
    except ImportError:
        # 最後備用：基本版本
        city_district_mapping = {
            "63000": {"name": "臺北市", "districts": {"63000030": "大安區"}},
            "64000": {"name": "高雄市", "districts": {"64000050": "三民區"}}
        }

def download_and_import_csv():
    """下載CSV並匯入資料庫"""
    local_csv_file = 'data/abc.csv'
    
    # 確保資料目錄存在
    os.makedirs('data', exist_ok=True)
    
    try:
        # 檢查本地檔案是否存在且在一個月內
        if os.path.exists(local_csv_file):
            file_time = os.path.getmtime(local_csv_file)
            current_time = datetime.now().timestamp()
            days_old = (current_time - file_time) / (24 * 3600)
            
            if days_old < 30:
                print(f"使用本地CSV檔案 (檔案建立於 {days_old:.1f} 天前)")
                return import_csv_to_database(local_csv_file)
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
        
        # 匯入資料庫
        return import_csv_to_database(local_csv_file)
        
    except Exception as e:
        print(f"處理CSV時發生錯誤: {e}")
        
        # 如果下載失敗，嘗試使用舊的本地檔案
        if os.path.exists(local_csv_file):
            print("下載失敗，使用現有的本地檔案...")
            return import_csv_to_database(local_csv_file)
        
        return False

def import_csv_to_database(csv_file):
    """將CSV資料匯入資料庫"""
    try:
        # 讀取CSV
        df = pd.read_csv(csv_file)
        df = df.dropna(subset=['機構名稱', '縣市', '區'])
        
        # 資料清理
        df['縣市'] = df['縣市'].astype(str)
        df['區'] = df['區'].astype(str).str.replace('.0', '', regex=False)
        
        # 清空現有資料
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM institutions')
        
        # 批次插入資料
        insert_count = 0
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO institutions (
                    name, code, type, city_code, district_code, address,
                    longitude, latitude, o_abc, service_type, contract_city,
                    contract_district, phone, email, manager, contract_start,
                    contract_end, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['機構名稱'], row['機構代碼'], row['機構種類'],
                row['縣市'], row['區'], row['地址全址'],
                row['經度'] if pd.notna(row['經度']) else None,
                row['緯度'] if pd.notna(row['緯度']) else None,
                row['O_ABC'], row['特約服務項目'], row['特約縣市'],
                row['特約區域'], row['機構電話'], row['電子郵件'],
                row['機構負責人姓名'], row['特約起日'], row['特約迄日'],
                row['最後異動時間']
            ))
            insert_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"✓ 成功匯入 {insert_count} 筆機構資料到資料庫")
        return True
        
    except Exception as e:
        print(f"匯入資料庫時發生錯誤: {e}")
        return False

def get_institution_count():
    """取得機構總數"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM institutions')
    count = cursor.fetchone()[0]
    conn.close()
    return count

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cities')
def get_cities():
    """取得所有縣市列表"""
    cities = [{"code": code, "name": data["name"]} 
              for code, data in city_district_mapping.items()]
    return jsonify(cities)

@app.route('/api/districts/<city_code>')
def get_districts(city_code):
    """根據縣市代碼取得區域列表"""
    if city_code in city_district_mapping:
        districts = [{"code": code, "name": name} 
                    for code, name in city_district_mapping[city_code]["districts"].items()]
        return jsonify(districts)
    return jsonify([])

@app.route('/api/institutions')
def search_institutions():
    """搜尋機構 - 資料庫版本"""
    city_code = request.args.get('city')
    district_code = request.args.get('district')
    service_type = request.args.get('service_type', '')
    
    # 建立SQL查詢
    where_conditions = []
    params = []
    
    # 縣市篩選
    if city_code:
        where_conditions.append('city_code = ?')
        params.append(city_code)
    
    # 鄉鎮區篩選 (地址模糊比對)
    if district_code:
        district_name = None
        if city_code in city_district_mapping:
            districts = city_district_mapping[city_code].get('districts', {})
            district_name = districts.get(district_code)
        
        if district_name:
            # 使用LIKE進行地址模糊比對
            where_conditions.append('(address LIKE ? OR address LIKE ?)')
            params.extend([f'%{district_name}%', f'%{district_name.replace("區", "").replace("市", "").replace("鎮", "").replace("鄉", "")}%'])
            print(f"使用區域名稱 '{district_name}' 進行資料庫地址模糊比對")
        else:
            where_conditions.append('district_code = ?')
            params.append(district_code)
    
    # 服務類型篩選
    if service_type:
        where_conditions.append('service_type LIKE ?')
        params.append(f'%{service_type}%')
    
    # 建立完整SQL
    sql = 'SELECT * FROM institutions'
    if where_conditions:
        sql += ' WHERE ' + ' AND '.join(where_conditions)
    sql += ' ORDER BY name LIMIT 100'
    
    # 執行查詢
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    
    # 計算總數 (不限制LIMIT)
    count_sql = 'SELECT COUNT(*) FROM institutions'
    if where_conditions:
        count_sql += ' WHERE ' + ' AND '.join(where_conditions)
    cursor.execute(count_sql, params)
    total_count = cursor.fetchone()[0]
    
    conn.close()
    
    # 轉換為字典格式
    result = []
    for row in rows:
        institution = {
            'name': row['name'],
            'code': row['code'],
            'type': row['type'],
            'city': row['city_code'],
            'district': row['district_code'],
            'address': row['address'],
            'longitude': row['longitude'],
            'latitude': row['latitude'],
            'service_type': row['service_type'],
            'phone': row['phone'],
            'email': row['email'],
            'manager': row['manager'],
            'contract_start': row['contract_start'],
            'contract_end': row['contract_end']
        }
        result.append(institution)
    
    print(f"資料庫查詢完成，找到 {total_count} 筆，返回前 {len(result)} 筆")
    
    return jsonify({
        'total': total_count,
        'institutions': result
    })

@app.route('/api/refresh-data')
def refresh_data():
    """強制重新下載並匯入資料"""
    # 刪除本地檔案以強制重新下載
    local_files = ['data/abc.csv']
    for file_path in local_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"已刪除 {file_path}")
    
    success = download_and_import_csv()
    if success:
        total_records = get_institution_count()
        file_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({
            "message": "資料強制更新成功", 
            "total_records": total_records,
            "update_time": file_time
        })
    else:
        return jsonify({"error": "資料更新失敗"}), 500

@app.route('/api/data-info')
def get_data_info():
    """取得資料檔案資訊"""
    local_csv_file = 'data/abc.csv'
    total_records = get_institution_count()
    
    info = {
        "local_file_exists": os.path.exists(local_csv_file),
        "total_records": total_records,
        "database_path": DATABASE_PATH,
        "database_exists": os.path.exists(DATABASE_PATH)
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
    print("=== 長照機構查詢系統 - SQLite 資料庫版本 ===")
    
    # 初始化資料庫
    init_database()
    
    # 載入縣市對照表
    load_city_district_mapping()
    print(f"✓ 載入 {len(city_district_mapping)} 個縣市對照表")
    
    # 檢查是否需要匯入資料
    record_count = get_institution_count()
    if record_count == 0:
        print("資料庫為空，開始匯入CSV資料...")
        download_and_import_csv()
        record_count = get_institution_count()
    
    print(f"✓ 資料庫中有 {record_count:,} 筆機構資料")
    print("✓ 系統啟動完成")
    print("🌐 請訪問: http://127.0.0.1:5000")
    
    app.run(debug=True, host='127.0.0.1', port=5000)