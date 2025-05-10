function toggleSort() {
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



function toggleCategories() {
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

function redirectToPage(url) {
  window.location.href = url; // Перенаправление на переданный URL
}


function redirectToProductsPageByCategory(categoryId) {
  const params = new URLSearchParams(window.location.search);
  let sort_param = params.get("sort");

  if (!sort_param) {
    sort_param = "created_at";
  }

  const baseUrl = window.location.origin; // http://127.0.0.1:8000
  const new_url = `${baseUrl}/products?category=${categoryId}&sort=${sort_param}`;

  redirectToPage(new_url);
}

function redirectToProductsPageBySort(sort) {
  const params = new URLSearchParams(window.location.search);
  let category_param = params.get("category");
  let search_param = params.get("search");
  const baseUrl = window.location.origin;

  if (search_param) {
    // Если есть параметр search, редиректим на /search/
    const new_url = `${baseUrl}/search/?search=${search_param}&sort=${sort}`;
    redirectToPage(new_url);
  } else {
    // Если параметр search отсутствует, редиректим на /products/
    if (!category_param) {
      redirectToPage(baseUrl);
    }
    const new_url = `${baseUrl}/products?category=${category_param}&sort=${sort}`;
    redirectToPage(new_url);
  }
}


function toggleChildren(event) {
  const parent = event.target;
  const categoryId = parent.dataset.categoryId;
  const childList = document.querySelector(`ul[data-parent-id='${categoryId}']`);
  
  if (childList) {
      childList.classList.toggle('hidden');
  }
}


