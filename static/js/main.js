// Handle navbar transparency on scroll
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
        } else {
            navbar.style.backgroundColor = 'white';
        }
    });

    // Product card click handler
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('click', function() {
            const link = this.querySelector('a') || this.dataset.href;
            if (link) {
                window.location.href = link;
            }
        });
    });

    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Initialize all carousels on the page
    const carousels = document.querySelectorAll('.vf-c-carousel');
    
    carousels.forEach(carousel => {
        const slides = carousel.querySelector('.vf-c-carousel__slides');
        const prevBtn = carousel.querySelector('.vf-c-carousel__nav--prev');
        const nextBtn = carousel.querySelector('.vf-c-carousel__nav--next');
        
        if (!slides || !prevBtn || !nextBtn) return;

        const slidesPerView = 4;
        const slideWidth = slides.querySelector('div')?.offsetWidth || 0;
        const gap = 32; // matches the gap in CSS

        function updateButtonVisibility() {
            const scrollLeft = slides.scrollLeft;
            const maxScroll = slides.scrollWidth - slides.clientWidth;

            prevBtn.disabled = scrollLeft <= 0;
            nextBtn.disabled = scrollLeft >= maxScroll;
        }

        function smoothScroll(element, target) {
            element.scrollTo({
                left: target,
                behavior: 'smooth'
            });
        }

        prevBtn.addEventListener('click', () => {
            const target = slides.scrollLeft - ((slideWidth + gap) * slidesPerView);
            smoothScroll(slides, target);
        });

        nextBtn.addEventListener('click', () => {
            const target = slides.scrollLeft + ((slideWidth + gap) * slidesPerView);
            smoothScroll(slides, target);
        });

        // Update button visibility on scroll and resize
        slides.addEventListener('scroll', updateButtonVisibility);
        window.addEventListener('resize', updateButtonVisibility);

        // Initial setup
        updateButtonVisibility();

        // Wishlist functionality for this carousel
        const wishlistButtons = carousel.querySelectorAll('.vf-c-product-card__wishlist');
        wishlistButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Toggle active class
                this.classList.toggle('active');
                
                // Get the heart icon SVG path
                const heartPath = this.querySelector('svg path');
                
                if (this.classList.contains('active')) {
                    // If active, fill the heart red
                    heartPath.setAttribute('fill', '#e11d48');
                    heartPath.setAttribute('stroke', '#e11d48');
                } else {
                    // If not active, remove the fill
                    heartPath.setAttribute('fill', 'none');
                    heartPath.setAttribute('stroke', 'currentColor');
                }
                
                // Add click animation
                this.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 200);
            });
        });
    });

    // Mega Menu functionality
    const nav = document.querySelector('nav');
    const megaMenu = document.getElementById('megaMenu');
    const navItems = document.querySelectorAll('[data-menu-target]');
    const menuContents = document.querySelectorAll('[data-menu-content]');
    let isMouseOverMenu = false;
    let activeNavItem = null;

    function showMegaMenu(navItem) {
        const menuTarget = navItem.getAttribute('data-menu-target');
        
        // First, make the mega menu visible
        megaMenu.classList.remove('hidden');
        megaMenu.classList.add('visible');
        
        // Then show the appropriate content
        menuContents.forEach(content => {
            if (content.getAttribute('data-menu-content') === menuTarget) {
                content.classList.remove('hidden');
                content.classList.add('flex');
            } else {
                content.classList.add('hidden');
                content.classList.remove('flex');
            }
        });
        
        activeNavItem = navItem;
    }

    function hideMegaMenu() {
        if (!isMouseOverMenu && !activeNavItem?.matches(':hover')) {
            megaMenu.classList.remove('visible');
            megaMenu.classList.add('hidden');
            
            menuContents.forEach(content => {
                content.classList.add('hidden');
                content.classList.remove('flex');
            });
            activeNavItem = null;
        }
    }

    // Event listeners for navigation items
    navItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            showMegaMenu(item);
        });
        
        item.addEventListener('mouseleave', () => {
            setTimeout(hideMegaMenu, 200);
        });
    });

    // Event listeners for mega menu
    megaMenu.addEventListener('mouseenter', () => {
        isMouseOverMenu = true;
    });

    megaMenu.addEventListener('mouseleave', () => {
        isMouseOverMenu = false;
        setTimeout(hideMegaMenu, 200);
    });

    // Close mega menu when clicking outside
    document.addEventListener('click', (event) => {
        if (!nav.contains(event.target)) {
            megaMenu.classList.remove('visible');
            megaMenu.classList.add('hidden');
            menuContents.forEach(content => {
                content.classList.add('hidden');
                content.classList.remove('flex');
            });
            activeNavItem = null;
        }
    });
});

   