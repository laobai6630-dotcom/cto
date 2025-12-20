// Dashboard主逻辑

document.addEventListener('DOMContentLoaded', function() {
    loadOverviewData();
    loadCandidates();
    
    document.getElementById('saveParamsBtn').addEventListener('click', saveParameters);
});

function loadOverviewData() {
    // TODO: 从API加载概览数据
    fetch('assets/data/overview.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('candidateCount').textContent = data.candidate_count || '-';
            document.getElementById('separationScore').textContent = data.separation_score ? data.separation_score.toFixed(4) : '-';
        })
        .catch(error => console.error('加载概览数据失败:', error));
}

function loadCandidates() {
    // TODO: 从API加载候选股票
    fetch('assets/data/candidates.json')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#candidatesTable tbody');
            tbody.innerHTML = '';
            
            data.forEach(candidate => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${candidate.stock_code}</td>
                    <td>${candidate.similarity.toFixed(4)}</td>
                    <td>${candidate.ml_score.toFixed(4)}</td>
                    <td>${candidate.chip_score.toFixed(4)}</td>
                `;
            });
        })
        .catch(error => console.error('加载候选股票失败:', error));
}

function saveParameters() {
    const threshold = document.getElementById('thresholdInput').value;
    
    // TODO: 保存参数到后端
    console.log('保存参数:', { threshold });
    alert('参数已保存');
}
