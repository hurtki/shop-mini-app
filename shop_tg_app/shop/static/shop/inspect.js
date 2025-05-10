// скрипт для свайпера 
const swiper = new Swiper('.swiper', {
loop: true, //  без автолистания
pagination: {
    el: '.swiper-pagination',
    clickable: true,
    type: 'fraction',
},
});



function getSelectedSize(sizeRadios) {
    let selectedSize = null;
    sizeRadios.forEach(radio => {
        if (radio.checked) {
            selectedSize = radio.value; // Получаем значение выбранного радиокнопки
        }
    });

    return selectedSize;
}


function generateTelegramLink(username, message) {
    // Кодируем сообщение с использованием encodeURIComponent
    const encodedMessage = encodeURIComponent(message);
    // Возвращаем ссылку
    return `https://t.me/${username}?text=${encodedMessage}`;
}

function handleBuyButton(product_id, product_price, product_name, username) {
    const sizeRadios = document.querySelectorAll('input[name="size"]');
    const warning = document.getElementById("size_pick_warning");
    selectedSize = getSelectedSize(sizeRadios);

    if (!selectedSize) {
        warning.style.display = "block";
        
    }
    else {
        warning.style.display = "none";
        const message = 
`👋 Здравствуйте! Хотел бы купить товар:
🛍️ Название: ${product_name}
💸 Цена: ${product_price}₽
📏 Размер: ${selectedSize}
🆔 Артикул: ${product_id}

📦 Можете помочь с заказом?`;

        // Генерируем ссылку для Telegram
        const telegramLink = generateTelegramLink(username, message.trim());

        // Открываем Telegram с предзаполненным сообщением
        window.open(telegramLink, "_blank");

        
    }
}

window.addEventListener('DOMContentLoaded', () => {
  if (!window.Telegram || !window.Telegram.WebApp) {
    console.warn('Telegram WebApp API недоступен');
    return;
  }

  const tg = window.Telegram.WebApp;

  // 🔑 Инициализируем WebApp
  tg.ready(); // <-- без этого BackButton не отобразится

  // Показываем кнопку "Назад"
  tg.BackButton.show();

  // Обработка нажатия
  tg.BackButton.onClick(() => {
    console.log('Нажата кнопка назад');

    if (window.history.length > 1) {
      window.history.back();
    } else {
      tg.close();
    }
  });

  // Разворачиваем WebApp
  tg.expand();
});
