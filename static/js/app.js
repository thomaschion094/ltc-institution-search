// 長照機構查詢系統 JavaScript

class LTCSearchApp {
    constructor() {
        this.apiBase = '/api';
        this.init();
    }

    async init() {
        await this.loadCities();
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchInstitutions();
        });
    }

    async loadCities() {
        try {
            const response = await fetch(`${this.apiBase}/cities`);
            const cities = await response.json();
            
            const citySelect = document.getElementById('citySelect');
            citySelect.innerHTML = '<option value="">請選擇縣市</option>';
            
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.code;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        } catch (error) {
            console.error('載入縣市資料失敗:', error);
            this.showAlert('載入縣市資料失敗', 'danger');
        }
    }

    async loadDistricts() {
        const cityCode = document.getElementById('citySelect').value;
        const districtSelect = document.getElementById('districtSelect');
        
        districtSelect.innerHTML = '<option value="">請選擇鄉鎮區</option>';
        
        if (!cityCode) return;

        try {
            const response = await fetch(`${this.apiBase}/districts/${cityCode}`);
            const districts = await response.json();
            
            districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district.code;
                option.textContent = district.name;
                districtSelect.appendChild(option);
            });
        } catch (error) {
            console.error('載入區域資料失敗:', error);
            this.showAlert('載入區域資料失敗', 'danger');
        }
    }

    async searchInstitutions() {
        const cityCode = document.getElementById('citySelect').value;
        const districtCode = document.getElementById('districtSelect').value;
        const serviceType = document.getElementById('serviceType').value;

        // 顯示載入指示器
        this.showLoading(true);
        this.hideStats();

        try {
            const params = new URLSearchParams();
            if (cityCode) params.append('city', cityCode);
            if (districtCode) params.append('district', districtCode);
            if (serviceType) params.append('service_type', serviceType);

            const response = await fetch(`${this.apiBase}/institutions?${params}`);
            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            this.displayResults(data.institutions);
            this.showStats(data.total);
        } catch (error) {
            console.error('搜尋失敗:', error);
            this.showAlert('搜尋失敗: ' + error.message, 'danger');
            this.displayResults([]);
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(institutions) {
        const container = document.getElementById('resultsContainer');
        
        if (institutions.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">沒有找到符合條件的機構</h5>
                    <p class="text-muted">請嘗試調整搜尋條件或選擇其他區域</p>
                </div>
            `;
            return;
        }

        const resultsHtml = institutions.map(institution => this.createInstitutionCard(institution)).join('');
        container.innerHTML = resultsHtml;
    }

    createInstitutionCard(institution) {
        const services = institution.service_type ? institution.service_type.split(';').map(s => s.trim()) : [];
        const serviceBadges = services.map(service => 
            `<span class="badge bg-primary service-badge">${service}</span>`
        ).join('');

        return `
            <div class="card result-card mb-3">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-8">
                            <h5 class="card-title">
                                <i class="fas fa-hospital text-primary"></i>
                                ${institution.name}
                            </h5>
                            <p class="card-text">
                                <i class="fas fa-map-marker-alt text-danger"></i>
                                ${institution.address}
                            </p>
                            <div class="mb-2">
                                ${serviceBadges}
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="text-md-end">
                                ${institution.phone ? `
                                    <p class="mb-1">
                                        <i class="fas fa-phone text-success"></i>
                                        <a href="tel:${institution.phone}" class="text-decoration-none">
                                            ${institution.phone}
                                        </a>
                                    </p>
                                ` : ''}
                                ${institution.email ? `
                                    <p class="mb-1">
                                        <i class="fas fa-envelope text-info"></i>
                                        <a href="mailto:${institution.email}" class="text-decoration-none">
                                            ${institution.email}
                                        </a>
                                    </p>
                                ` : ''}
                                ${institution.manager ? `
                                    <p class="mb-1">
                                        <i class="fas fa-user text-secondary"></i>
                                        ${institution.manager}
                                    </p>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                    <div class="row mt-2">
                        <div class="col-12">
                            <small class="text-muted">
                                機構代碼: ${institution.code} | 
                                特約期間: ${institution.contract_start} ~ ${institution.contract_end}
                            </small>
                        </div>
                    </div>
                    ${institution.longitude && institution.latitude ? `
                        <div class="mt-2">
                            <button class="btn btn-outline-primary btn-sm" onclick="showMap(${institution.latitude}, ${institution.longitude}, '${institution.name}')">
                                <i class="fas fa-map"></i> 查看地圖
                            </button>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    showStats(total) {
        document.getElementById('totalCount').textContent = total.toLocaleString();
        document.getElementById('statsContainer').style.display = 'block';
    }

    hideStats() {
        document.getElementById('statsContainer').style.display = 'none';
    }

    showLoading(show) {
        const indicator = document.getElementById('loadingIndicator');
        indicator.style.display = show ? 'block' : 'none';
    }

    showAlert(message, type = 'info') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.getElementById('resultsContainer');
        container.innerHTML = alertHtml + container.innerHTML;
    }
}

// 全域函數
function loadDistricts() {
    app.loadDistricts();
}

function showMap(lat, lng, name) {
    const url = `https://www.google.com/maps?q=${lat},${lng}&z=15&t=m`;
    window.open(url, '_blank');
}

async function showDataInfo() {
    try {
        const response = await fetch('/api/data-info');
        const data = await response.json();
        
        let statusHtml = '';
        if (data.local_file_exists) {
            const statusClass = data.needs_update ? 'text-warning' : 'text-success';
            const statusIcon = data.needs_update ? 'exclamation-triangle' : 'check-circle';
            const statusText = data.needs_update ? '需要更新' : '資料最新';
            
            statusHtml = `
                <div class="row">
                    <div class="col-md-6">
                        <p class="mb-1">
                            <i class="fas fa-calendar"></i> 
                            <strong>檔案日期:</strong> ${data.file_date}
                        </p>
                        <p class="mb-1">
                            <i class="fas fa-clock"></i> 
                            <strong>檔案年齡:</strong> ${data.days_old} 天
                        </p>
                    </div>
                    <div class="col-md-6">
                        <p class="mb-1">
                            <i class="fas fa-database"></i> 
                            <strong>記錄數量:</strong> ${data.total_records.toLocaleString()} 筆
                        </p>
                        <p class="mb-1 ${statusClass}">
                            <i class="fas fa-${statusIcon}"></i> 
                            <strong>狀態:</strong> ${statusText}
                        </p>
                    </div>
                </div>
                <div class="mt-2">
                    <small class="text-muted">
                        <i class="fas fa-info-circle"></i> 
                        系統每30天自動更新一次資料，您也可以手動強制更新
                    </small>
                </div>
            `;
        } else {
            statusHtml = `
                <p class="text-warning mb-0">
                    <i class="fas fa-exclamation-triangle"></i> 
                    本地資料檔案不存在，將在首次搜尋時自動下載
                </p>
            `;
        }
        
        document.getElementById('dataInfoContent').innerHTML = statusHtml;
        document.getElementById('dataInfoContainer').style.display = 'block';
        
        // 3秒後自動隱藏
        setTimeout(() => {
            document.getElementById('dataInfoContainer').style.display = 'none';
        }, 5000);
        
    } catch (error) {
        app.showAlert('無法取得資料狀態: ' + error.message, 'danger');
    }
}

async function refreshData() {
    if (!confirm('確定要強制重新下載資料嗎？這將刪除現有的本地檔案並重新下載最新資料。')) {
        return;
    }
    
    try {
        app.showLoading(true);
        const response = await fetch('/api/refresh-data');
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        app.showAlert(`資料強制更新成功！共載入 ${data.total_records.toLocaleString()} 筆機構資料<br>更新時間: ${data.update_time}`, 'success');
    } catch (error) {
        app.showAlert('資料更新失敗: ' + error.message, 'danger');
    } finally {
        app.showLoading(false);
    }
}

// 初始化應用程式
const app = new LTCSearchApp();