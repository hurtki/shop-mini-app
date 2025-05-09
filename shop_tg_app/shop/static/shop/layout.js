function toggleSort() {
  const input = document.getElementById("sortings");

  if (input.style.display === "none" || input.style.display === "") {
    input.style.display = "block";
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


function redirectToProductsPage(categoryId, baseUrl) {
  const params = new URLSearchParams(window.location.search);
  let sort_param = params.get("sort");

  if (!sort_param) {
    sort_param = "created_at";
  }

  const new_url = `http://${baseUrl}/products?category=${categoryId}&sort=${sort_param}`;

  window.location.href = new_url;
}

function open_children() {

}

function toggleChildren(event) {
  console.log("зашли в ф");
  const parent = event.target;
  const categoryId = parent.dataset.categoryId;
  const childList = document.querySelector(`ul[data-parent-id='${categoryId}']`);
  
  if (childList) {
      console.log("test")
      childList.classList.toggle('hidden');
  }
}
