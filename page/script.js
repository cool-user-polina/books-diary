const API_BASE = 'http://127.0.0.1:5000'; // Базовый URL для API
const bookList = document.getElementById('book-list'); // Элемент списка книг
const bookDetail = document.getElementById('book-detail'); // Элемент с деталями книги
const backButton = document.getElementById('back-button'); // Кнопка "Назад"
const bookTitle = document.getElementById('book-title'); // Название книги
const bookAuthor = document.getElementById('book-author'); // Автор книги
const bookDescription = document.getElementById('book-description'); // Описание книги

// Получение и отображение списка книг
async function fetchBooks() {
    const response = await fetch(`${API_BASE}/books`); // Запрос к API
    const books = await response.json();
    bookList.innerHTML = ''; // Очищаем список
    books.forEach(book => {
        const li = document.createElement('li'); // Создаем элемент списка
        li.textContent = `${book.name} - ${book.author}`;
        li.onclick = () => fetchBookDetail(book.id); // Навешиваем обработчик клика
        bookList.appendChild(li); // Добавляем элемент в список
    });
}

//получение и отображение деталей книги
async function fetchBookDetail(id) {
    const response = await fetch(`${API_BASE}/books/${id}`); // Запрос к API
    const book = await response.json();
    if (book.error) {
        alert(book.error); // Выводим ошибку, если книга не найдена
        return;
    }
    bookList.classList.add('hidden'); // Скрываем список книг
    bookDetail.classList.remove('hidden'); // Показываем детали книги
    bookTitle.textContent = book.title; // Устанавливаем название книги
    bookAuthor.textContent = `Автор: ${book.author}`; // Устанавливаем автора книги
    bookDescription.textContent = book.description; // Устанавливаем описание книги
}

// Обработчик для кнопки "Назад"
backButton.onclick = () => {
    bookDetail.classList.add('hidden'); // Скрываем детали книги
    bookList.classList.remove('hidden'); // Показываем список книг
};

// Инициализация приложения
fetchBooks();
