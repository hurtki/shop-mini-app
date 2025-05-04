// скрипт для свайпера 
const swiper = new Swiper('.swiper', {
loop: true, // ❌ без автолистания
pagination: {
    el: '.swiper-pagination',
    clickable: true,
    type: 'fraction',
},
});
