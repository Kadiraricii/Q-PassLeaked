// script.js (replace the entire content)
document.addEventListener('DOMContentLoaded', function() {
    // Load theme preference
    const theme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(theme);
    updateThemeIcon(theme);

    // Theme toggle
    document.getElementById('theme-toggle').addEventListener('click', function() {
        const newTheme = document.body.classList.contains('light') ? 'dark' : 'light';
        document.body.classList.remove('light', 'dark');
        document.body.classList.add(newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    // Language change
    document.getElementById('language').addEventListener('change', changeLanguage);

    // Tutorial button (if present)
    const showTutorialBtn = document.getElementById('show-tutorial');
    if (showTutorialBtn) {
        showTutorialBtn.addEventListener('click', function() {
            const lang = document.getElementById('language').value;
            fetch(`/tutorial/${lang}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('tutorial-content').innerHTML = data.description.replace(/\n/g, '<br>');
                    document.getElementById('tutorial-content').style.display = 'block';
                })
                .catch(error => console.error('Error loading tutorial:', error));
        });
    }
});

function changeLanguage() {
    const lang = document.getElementById('language').value;
    const currentPath = window.location.pathname;
    const newUrl = `${currentPath}${window.location.search ? '&' : '?'}lang=${lang}`;
    window.location.href = newUrl;
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.innerHTML = theme === 'light' ? '🌙' : '☀️'; // Moon for dark, Sun for light
}

// Service worker registration
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
        .then(reg => console.log('Service Worker registered', reg))
        .catch(err => console.log('Service Worker registration failed', err));
}