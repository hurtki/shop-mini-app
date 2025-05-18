function getNoSizeMessage(product_name, product_price, product_id) {
    return `👋 Здравствуйте! Хотел бы купить товар:
🛍️ Название: ${product_name}
💸 Цена: ${product_price}₽
🆔 Артикул: ${product_id}`;
}

function getSizeMessage(product_name, product_price, selectedSize, product_id) {
    return `👋 Здравствуйте! Хотел бы купить товар:
🛍️ Название: ${product_name}
💸 Цена: ${product_price}₽
📏 Размер: ${selectedSize}
🆔 Артикул: ${product_id}`;
}

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
    selectedSize = getSelectedSize(sizeRadios);
    
    // если не выбран размер то дефолтное сообщение подставляем
    const message = selectedSize
        ? getSizeMessage(product_name, product_price, selectedSize, product_id)
        : getNoSizeMessage(product_name, product_price, product_id);

    // Генерируем ссылку для Telegram
    const telegramLink = generateTelegramLink(username, message.trim());

    // Открываем Telegram с предзаполненным сообщением
    window.open(telegramLink, "_blank");

}

// перменная для хранения последнего нажатого радио
let lastChecked = null;
// обработчик клика по радио кнопке
// добавляет возможность отжатия кнопки при повтороном нажатии 
function toggleRadio(radio) {
if (lastChecked === radio) {
    radio.checked = false;
    lastChecked = null;
} else {
    lastChecked = radio;
}
}




// tg mini app back button logic 
Telegram.WebApp.ready();


// обработчик кнопки назад 
Telegram.WebApp.onEvent('backButtonClicked', function() {
  console.log('Back button clicked, entered func on event backButtonClicked');
  // получаем из session storage предыдущую страницу 
  const back = sessionStorage.getItem('prevPage') || '/';
  // прячем кнопку назад 
  Telegram.WebApp.BackButton.hide();
  redirectToPage(back);
});



// изначально показываем кнопку назад 
Telegram.WebApp.BackButton.show();

