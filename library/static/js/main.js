// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления карточек
    const cards = document.querySelectorAll('.book-card, .author-card, .genre-card');
    cards.forEach((card, i) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, i * 50);
    });

    // Плавное появление страницы
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s';
    document.body.style.opacity = '1';

    // Парящие 3D карточки
    const hoverCards = document.querySelectorAll('.book-card, .author-card');
    hoverCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // Анимированный фон для header
    const header = document.querySelector('.header');
    if (header) {
        let hue = 0;
        setInterval(() => {
            hue = (hue + 1) % 360;
            header.style.transition = 'background 0.1s';
            header.style.background = `linear-gradient(135deg, #5d4037, hsl(${hue}, 30%, 30%))`;
        }, 50);
    }

    // Кнопка "Наверх"
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #5d4037;
        color: white;
        border: none;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        font-size: 24px;
        cursor: pointer;
        display: none;
        z-index: 999;
        transition: all 0.3s;
    `;
    document.body.appendChild(scrollBtn);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });
    
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Подсветка строки поиска
    const searchInput = document.querySelector('.search-form input');
    if (searchInput) {
        searchInput.addEventListener('focus', () => {
            searchInput.style.borderColor = '#ffab91';
            searchInput.style.boxShadow = '0 0 5px rgba(255,171,145,0.3)';
        });
        searchInput.addEventListener('blur', () => {
            searchInput.style.borderColor = '#444';
            searchInput.style.boxShadow = 'none';
        });
    }

    // Живой поиск (фильтрация книг)
    const searchInputLive = document.getElementById('searchInput');
    if (searchInputLive) {
        searchInputLive.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const books = document.querySelectorAll('.book-card');
            let visibleCount = 0;
            
            books.forEach(book => {
                const title = book.querySelector('h3')?.textContent.toLowerCase() || '';
                const author = book.querySelector('.book-meta')?.textContent.toLowerCase() || '';
                
                if (title.includes(query) || author.includes(query)) {
                    book.style.display = '';
                    visibleCount++;
                } else {
                    book.style.display = 'none';
                }
            });
            
            const resultInfo = document.getElementById('searchResult');
            if (resultInfo) {
                resultInfo.textContent = `Найдено книг: ${visibleCount}`;
            }
        });
    }

    // Прогресс скролла
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        
        let progressBar = document.getElementById('progressBar');
        if (!progressBar) {
            progressBar = document.createElement('div');
            progressBar.id = 'progressBar';
            progressBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 0%;
                height: 3px;
                background: #ffab91;
                z-index: 9999;
                transition: width 0.1s;
            `;
            document.body.appendChild(progressBar);
        }
        progressBar.style.width = scrolled + '%';
    });

    // Уведомление при добавлении в избранное
    window.showNotification = function(message) {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #5d4037;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    };

    // AJAX для избранного
    window.toggleFavorite = function(bookId, button) {
        fetch(`/book/${bookId}/favorite/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_favorite) {
                button.innerHTML = '❤️ В избранном';
                button.style.background = '#ffab91';
                button.style.color = '#1a1a1a';
                showNotification('Добавлено в избранное');
            } else {
                button.innerHTML = '🤍 В избранное';
                button.style.background = '#444';
                button.style.color = '#e0e0e0';
                showNotification('Удалено из избранного');
            }
        });
    };

    // Случайные цитаты о книгах
    const quotes = [
        '📚 "Книга - мечта, которую ты держишь в руках"',
        '📖 "Чтение - это путешествие без билета"',
        '🌟 "Книги делают нас лучше"',
        '🎯 "Читай, чтобы жить ярче"',
        '💫 "Каждая книга - новая жизнь"'
    ];
    
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    const footer = document.querySelector('.footer .container');
    if (footer && !document.querySelector('.quote')) {
        const quoteDiv = document.createElement('div');
        quoteDiv.className = 'quote';
        quoteDiv.textContent = randomQuote;
        quoteDiv.style.cssText = `
            margin-top: 10px;
            font-size: 12px;
            opacity: 0.7;
            font-style: italic;
        `;
        footer.appendChild(quoteDiv);
    }

    // Подтверждение выхода
    window.confirmLogout = function() {
        if (confirm('Вы уверены, что хотите выйти?')) {
            document.getElementById('logout-form')?.submit();
        }
        return false;
    };
});

// Стили для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .book-card, .author-card {
        transition: transform 0.1s ease;
        transform-style: preserve-3d;
    }
`;
document.head.appendChild(style);