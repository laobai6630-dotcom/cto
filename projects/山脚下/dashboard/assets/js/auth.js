// 身份验证逻辑

let isAuthenticated = false;

document.getElementById('loginBtn').addEventListener('click', function() {
    if (isAuthenticated) {
        logout();
    } else {
        login();
    }
});

function login() {
    const password = prompt('请输入密码:');
    
    // TODO: 实际密码验证
    if (password === 'admin123') {
        isAuthenticated = true;
        document.getElementById('loginBtn').textContent = '登出';
        document.getElementById('saveParamsBtn').disabled = false;
        alert('登录成功！');
    } else {
        alert('密码错误！');
    }
}

function logout() {
    isAuthenticated = false;
    document.getElementById('loginBtn').textContent = '登录';
    document.getElementById('saveParamsBtn').disabled = true;
    alert('已登出');
}
