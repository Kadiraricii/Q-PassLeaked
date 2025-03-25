document.addEventListener('DOMContentLoaded', function() {
    // Theme initialization
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        const theme = localStorage.getItem('theme') || 'light';
        document.body.classList.add(theme);
        updateThemeIcon(theme);

        themeToggle.addEventListener('click', function() {
            const newTheme = document.body.classList.contains('light') ? 'dark' : 'light';
            document.body.classList.remove('light', 'dark');
            document.body.classList.add(newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    } else {
        console.warn('Theme toggle button not found.');
    }

    // Language switching for TR | EN links
    const languageLinks = document.querySelectorAll('.language-switcher a');
    if (languageLinks.length > 0) {
        languageLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const lang = this.textContent.trim(); // 'EN' or 'TR'
                const currentUrl = new URL(window.location.href);
                currentUrl.searchParams.set('lang', lang);
                window.location.href = currentUrl.toString();
            });
        });
    } else {
        console.warn('Language switcher links not found.');
    }
});

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️';
    }
}