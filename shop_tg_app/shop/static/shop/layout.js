const slides = [
    { img: 'static/shop/pics/base_shirts/shirt1.jpeg', url: 'https://example.com/1' },
    { img: 'static/shop/pics/base_shirts/shirt2.jpeg', url: 'https://example.com/2' },
    { img: 'static/shop/pics/base_shirts/shirt3.jpeg', url: 'https://example.com/3' }
  ];
  
  let index = 0;
  const sliderImg = document.getElementById('slider-image');
  const sliderLink = document.getElementById('slider-link');
  
  setInterval(() => {
    index = (index + 1) % slides.length;
    sliderImg.style.opacity = 0;
  
    setTimeout(() => {
      sliderImg.src = slides[index].img;
      sliderLink.href = slides[index].url;
      sliderImg.style.opacity = 1;
    }, 500);
  }, 3000);
  