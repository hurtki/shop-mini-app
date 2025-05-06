function toggleSort() {
  const input = document.getElementById("sortings");

  if (input.style.display === "none" || input.style.display === "") {
    input.style.display = "block";
    input.style.zIndex = 999;
  } else {
    input.style.display = "none";
  }
}

