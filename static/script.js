document.addEventListener('DOMContentLoaded', function() {
    const theme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(theme);
    updateThemeIcon(theme);

    document.getElementById('theme-toggle').addEventListener('click', function() {
        const newTheme = document.body.classList.contains('light') ? 'dark' : 'light';
        document.body.classList.remove('light', 'dark');
        document.body.classList.add(newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    document.getElementById('language').addEventListener('change', changeLanguage);
});

function changeLanguage() {
    const lang = document.getElementById('language').value;
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('lang', lang);
    window.location.href = currentUrl.toString();
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️';
}