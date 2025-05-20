// откртие окна сортировки 
function toggleSort() {
  const categories_input = document.getElementById("categories");
  
  if (categories_input.style.display === "block") {
    return;
  }
  
  const input = document.getElementById("sortings");
  const params = new URLSearchParams(window.location.search);
  
  if (input.style.display === "none" || input.style.display === "") {
    input.style.display = "block";
    const sort = params.get('sort'); 

    const selector = sort ? `.sort${sort}` : `.sort-created_at`;
    const el = document.querySelector(selector);

    
    el.style.border = "2px solid white";

    input.style.zIndex = 999;
  } else {
    input.style.display = "none";
  }
}


// открытие окна категорий 
function toggleCategories() {
  const sortings_input = document.getElementById("sortings");
  
  if (sortings_input.style.display === "block") {
    return;
  }

  const input = document.getElementById("categories");

  if (input.style.display === "none" || input.style.display === "") {
    input.style.display = "block";
    input.style.zIndex = 999;
    changeCategoryIcon()
  } else {
    input.style.display = "none";
    changeCategoryIcon()
  }
}


// ГЛАВНАЯ ФУНКЦИЯ ДЛЯ ПЕРЕХОДА НА ДРУГУЮ СТРАНИЦУ
function redirectToPage(url) {
  // сохраняем текущую страницу в session storage 
  // для последующей реализации кнопки back 
  const cleanUrl = window.location.origin + window.location.pathname + window.location.search;
  sessionStorage.setItem('prevPage', cleanUrl);

  Telegram.WebApp.BackButton.hide(); // прячем кнопку назад
  // сохраняем полный URL
  
  window.location.href = url; // Перенаправление на переданный URL
}

// применение категории из окна категорий 
function redirectToProductsPageByCategory(categoryId) {
  const params = new URLSearchParams(window.location.search);
  let sort_param = params.get("sort");
  // если нету параметра в url на странице на которой мы находимся то ставим дефолтный 
  if (!sort_param) {
    sort_param = "-created_at";
  }
  
  const baseUrl = window.location.origin; 
  const new_url = `${baseUrl}/products?category=${categoryId}&sort=${sort_param}`;

  redirectToPage(new_url);
}


// применение категории из окна сортировок 
function redirectToProductsPageBySort(sort) {
  const params = new URLSearchParams(window.location.search);
  let category_param = params.get("category");
  let search_param = params.get("search");
  const baseUrl = window.location.origin;

  // проверяем находимся ли сы на странице поиска 
  if (search_param) {
    // Если есть параметр search, редиректим на /search/
    const new_url = `${baseUrl}/search/?search=${search_param}&sort=${sort}`;
    redirectToPage(new_url);
    return;
  } else {
    // Если параметр search отсутствует, редиректим на /products/
    if (!category_param) {
      const new_url = `${baseUrl}?sort=${sort}`;
      redirectToPage(new_url);
      return;
    }
    const new_url = `${baseUrl}/products?category=${category_param}&sort=${sort}`;
    redirectToPage(new_url);
  }
}

// делает видными всех ul детей у объекта 
function toggleChildren(event) {
  const parent = event.target;
  const categoryId = parent.dataset.categoryId;
  const childList = document.querySelector(`ul[data-parent-id='${categoryId}']`);
  
  if (childList) {
      childList.classList.toggle('hidden');
  }
}




const search_input = document.getElementById("search_field");

// при отправке поиска
function handleSearchSend() {
  
  const input_value = search_input.value.trim();

  // проводим валидацию по длинне инпута 
  if ((input_value.length < search_input.minLength) || (input_value.length > search_input.maxLength)) {
    const search_bar_frame = document.getElementById("search_bar");
    console.log("entered handlesearch");
    search_bar_frame.style.border = "solid 1.7px var(--warning-color-dim)";
    return;
  } 

  // генерируем url для переадресовки 
  const baseUrl = window.location.origin;
  const new_url = `${baseUrl}/search/?search=${encodeURIComponent(input_value)}`;
  redirectToPage(new_url);
}


// вегшаем на инпут поиска если нажата кнопка и проверяем была ли это кнопка отправки 
// если это была кнопка отправки то вызываем функцию отправки 
search_input.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    handleSearchSend();
  }
});

const app = window.Telegram?.WebApp;
// убирание вертикального свайпа в веб приложении для закрытия
if (app) {
  app.ready();

  // 2. Попытка использовать актуальные методы Telegram API
  if (typeof app.disableVerticalSwipes === 'function') {
    app.disableVerticalSwipes(); 
  }

  // 3. Возможно, работает кастомная настройка (для некоторых клиентов)
  if (typeof app.setOption === 'function') {
    try {
      app.setOption('allow_vertical_swipe', false);
    } catch (e) {
      console.warn("setOption не сработал:", e);
    }
  }
} else {
  console.warn("Telegram.WebApp не найден");
}