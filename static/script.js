document.addEventListener('DOMContentLoaded', function() {
    // Load theme preference
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.add('light');
    }

    // Theme toggle
    document.getElementById('theme-toggle').addEventListener('click', function() {
        if (document.body.classList.contains('light')) {
            document.body.classList.remove('light');
            document.body.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark');
            document.body.classList.add('light');
            localStorage.setItem('theme', 'light');
        }
    });

    // Language change
    document.getElementById('language').addEventListener('change', changeLanguage);
});

function changeLanguage() {
    const lang = document.getElementById('language').value;
    const currentPath = window.location.pathname;
    if (currentPath === '/about') {
        window.location.href = `/about?lang=${lang}`;
    } else {
        // For other pages, reload with selected language if needed
        document.getElementById('language-form').value = lang; // Sync form select if present
    }
}

// Service worker registration
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
        .then(reg => console.log('Service Worker registered', reg))
        .catch(err => console.log('Service Worker registration failed', err));
}