// 国际化支持

const translations = {
    zh_CN: null,
    en_US: null
};

let currentLang = 'zh_CN';

// 加载翻译文件
fetch('../locales/zh_CN.json')
    .then(r => r.json())
    .then(data => translations.zh_CN = data);

fetch('../locales/en_US.json')
    .then(r => r.json())
    .then(data => translations.en_US = data);

document.getElementById('langSelect').addEventListener('change', function(e) {
    currentLang = e.target.value;
    updateLanguage();
});

function updateLanguage() {
    // TODO: 更新页面语言
    if (translations[currentLang]) {
        console.log('切换语言:', currentLang);
    }
}
