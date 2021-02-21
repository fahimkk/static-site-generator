// Resent blog
$('#owl-carousel-1').owlCarousel({
    autoplay: true,
    autoplayHoverPause: true,
    loop: true,
    items:3,
    nav: true,
    dots: true,
    responsive:{
    // display resolution
        0:{
            items: 1, 
            dots: false,
        },
        485: {
            items: 1,
        },
        728: {
            items: 2,
        },
        960: {
            items: 2,
        },
        1200: {
            items: 3,
        }
    }
});

// Projects
$('#owl-carousel-2').owlCarousel({
    autoplay: true,
    autoplayHoverPause: true,
    loop: true,
    // for responsive
    lazyLoad: true,
    margin:30,
    stagePadding: 4,
    nav:true,
    dots:true,
    responsive:{
    // display resolution
        0:{
            items: 1, 
            nav: false
        },
        485: {
            items: 1,
            dots: false
        },
        728: {
            items: 2,
        },
        960: {
            items: 2,
        },
        1200: {
            items: 2,
        }
    }
});

// Cheatsheet
$('#owl-carousel-3').owlCarousel({
    autoplay: true,
    autoplayHoverPause: true,
    loop: true,
    lazyLoad: true,
    margin:30,
    stagePadding: 4,
    dots:true,
    nav:true,
    responsive:{
    // display resolution
        0:{
            items: 1, 
            nav: false
        },
        485: {
            items: 2,
        },
        728: {
            items: 2,
            loop: true
        },
        960: {
            items: 3,
            loop:true
        },
        1200: {
            items: 4,
        }
    }
});

