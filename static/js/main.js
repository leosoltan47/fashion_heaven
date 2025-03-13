// Handle navbar transparency on scroll
document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 50) {
      navbar.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
    } else {
      navbar.style.backgroundColor = "white";
    }
  });

  // Product card click handler
  const productCards = document.querySelectorAll(".product-card");
  productCards.forEach((card) => {
    card.addEventListener("click", function () {
      const link = this.querySelector("a") || this.dataset.href;
      if (link) {
        window.location.href = link;
      }
    });
  });

  // Initialize Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]'),
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth",
      });
    });
  });

  // Initialize all carousels on the page
  const carousels = document.querySelectorAll(".vf-c-carousel");

  carousels.forEach((carousel) => {
    const slides = carousel.querySelector(".vf-c-carousel__slides");
    const prevBtn = carousel.querySelector(".vf-c-carousel__nav--prev");
    const nextBtn = carousel.querySelector(".vf-c-carousel__nav--next");

    if (!slides || !prevBtn || !nextBtn) return;

    const slidesPerView = 4;
    const slideWidth = slides.querySelector("div")?.offsetWidth || 0;
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
        behavior: "smooth",
      });
    }

    prevBtn.addEventListener("click", () => {
      const target = slides.scrollLeft - ((slideWidth + gap) * slidesPerView);
      smoothScroll(slides, target);
    });

    nextBtn.addEventListener("click", () => {
      const target = slides.scrollLeft + ((slideWidth + gap) * slidesPerView);
      smoothScroll(slides, target);
    });

    // Update button visibility on scroll and resize
    slides.addEventListener("scroll", updateButtonVisibility);
    window.addEventListener("resize", updateButtonVisibility);

    // Initial setup
    updateButtonVisibility();

    // Wishlist functionality for this carousel
    const wishlistButtons = carousel.querySelectorAll(
      ".vf-c-product-card__wishlist",
    );
    wishlistButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();

        // Toggle active class
        this.classList.toggle("active");

        // Get the heart icon SVG path
        const heartPath = this.querySelector("svg path");

        if (this.classList.contains("active")) {
          // If active, fill the heart red
          heartPath.setAttribute("fill", "#e11d48");
          heartPath.setAttribute("stroke", "#e11d48");
        } else {
          // If not active, remove the fill
          heartPath.setAttribute("fill", "none");
          heartPath.setAttribute("stroke", "currentColor");
        }

        // Add click animation
        this.style.transform = "scale(1.2)";
        setTimeout(() => {
          this.style.transform = "scale(1)";
        }, 200);
      });
    });
  });

  // Mega Menu functionality
  const nav = document.querySelector("nav");
  const navContainer = document.querySelector(".nav-mega-container");
  const megaMenu = document.getElementById("megaMenu");
  const navItems = document.querySelectorAll("[data-menu-target]");
  const menuContents = document.querySelectorAll("[data-menu-content]");
  let isMouseOverMenu = false;
  let activeNavItem = null;

  // Apply the fixed width styling to all mega menu content containers once on page load
  menuContents.forEach((content) => {
    content.style.cssText = `
            width: 1488px !important;
            max-width: 1488px !important;
            margin: 0 auto !important;
            padding: 2rem !important;
            background-color: white !important;
            box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1) !important;
        `;
  });

  function showMegaMenu(navItem) {
    const menuTarget = navItem.getAttribute("data-menu-target");

    // Make mega menu visible and enforce styling
    megaMenu.classList.remove("hidden");
    megaMenu.style.cssText = `
            position: absolute !important;
            top: 100% !important;
            left: 0 !important;
            right: 0 !important;
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            background-color: transparent !important;
            z-index: 40 !important;
            border-top: 1px solid #e5e7eb !important;
        `;

    // Force display before adding visible class to ensure transition works
    window.getComputedStyle(megaMenu).display;

    megaMenu.classList.add("visible");

    // Show the appropriate content
    menuContents.forEach((content) => {
      if (content.getAttribute("data-menu-content") === menuTarget) {
        content.classList.remove("hidden");
        content.classList.add("flex");

        // All menus use the same full width now
        content.style.cssText = `
                    display: flex !important;
                    width: 1488px !important;
                    max-width: 1488px !important;
                    margin: 0 auto !important;
                    padding: 2rem !important;
                    background-color: white !important;
                    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1) !important;
                `;

        // Special case for new-featured menu grid columns
        if (menuTarget === "new-featured") {
          // Update grid columns for new-featured
          const categoryLists = content.querySelectorAll(
            ".DesktopSubNav_sub-menu-category-list",
          );
          categoryLists.forEach((list) => {
            list.style.cssText = `
                            list-style: none !important;
                            padding: 0 !important;
                            margin: 0 !important;
                            width: 100% !important;
                            display: grid !important;
                            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                            gap: 2rem !important;
                        `;
          });
        }

        // Ensure all banner images are properly styled
        const banners = content.querySelectorAll(".b-navigation-banner");
        banners.forEach((banner) => {
          const container = banner.querySelector(
            ".b-navigation_banner-container",
          );
          if (container) {
            container.style.cssText = `
                            display: flex !important;
                            flex-direction: column !important;
                            height: 100% !important;
                        `;
          }

          const image = banner.querySelector(".b-navigation_banner-image");
          if (image) {
            image.style.cssText = `
                            width: 100% !important;
                            height: auto !important;
                            border-radius: 8px !important;
                            object-fit: cover !important;
                        `;
          }
        });

        // Style all category lists
        const categoryLists = content.querySelectorAll(
          ".DesktopSubNav_sub-menu-category-list",
        );
        categoryLists.forEach((list) => {
          list.style.cssText = `
                        list-style: none !important;
                        padding: 0 !important;
                        margin: 0 !important;
                        width: 100% !important;
                        display: grid !important;
                        grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
                        gap: 2rem !important;
                    `;
        });

        // Ensure all category groupings are properly styled
        const categoryGroupings = content.querySelectorAll(
          ".DesktopSubNav_sub-menu-category-grouping",
        );
        categoryGroupings.forEach((list) => {
          list.style.cssText = `
                        list-style: none !important;
                        padding: 0 !important;
                        margin: 0 !important;
                        display: flex !important;
                        flex-direction: column !important;
                        gap: 12px !important;
                    `;
        });

        // Ensure all category titles are properly styled
        const categoryTitles = content.querySelectorAll(
          ".DesktopSubNav_sub-menu-category-title",
        );
        categoryTitles.forEach((title) => {
          title.style.cssText = `
                        font-size: 14px !important;
                        font-weight: 600 !important;
                        text-transform: uppercase !important;
                        letter-spacing: 0.5px !important;
                        color: #111827 !important;
                        margin-bottom: 16px !important;
                        display: block !important;
                        text-decoration: none !important;
                    `;
        });
      } else {
        content.classList.add("hidden");
        content.classList.remove("flex");
        content.style.display = "none";
      }
    });

    activeNavItem = navItem;
  }

  function hideMegaMenu() {
    if (!isMouseOverMenu && !activeNavItem?.matches(":hover")) {
      megaMenu.classList.remove("visible");
      setTimeout(() => {
        if (!isMouseOverMenu && !activeNavItem?.matches(":hover")) {
          megaMenu.classList.add("hidden");
          megaMenu.style.display = "none";

          menuContents.forEach((content) => {
            content.classList.add("hidden");
            content.classList.remove("flex");
            content.style.display = "none";
          });
        }
      }, 300); // Match the transition duration in CSS

      activeNavItem = null;
    }
  }

  // Event listeners for navigation items
  navItems.forEach((item) => {
    item.addEventListener("mouseenter", () => {
      showMegaMenu(item);
    });

    item.addEventListener("mouseleave", () => {
      setTimeout(hideMegaMenu, 200);
    });
  });

  // Event listeners for mega menu
  megaMenu.addEventListener("mouseenter", () => {
    isMouseOverMenu = true;
  });

  megaMenu.addEventListener("mouseleave", () => {
    isMouseOverMenu = false;
    setTimeout(hideMegaMenu, 200);
  });

  // Close mega menu when clicking outside
  document.addEventListener("click", (event) => {
    if (!nav.contains(event.target)) {
      megaMenu.classList.remove("visible");
      setTimeout(() => {
        megaMenu.classList.add("hidden");
      }, 300);

      menuContents.forEach((content) => {
        content.classList.add("hidden");
        content.classList.remove("flex");
        content.style.display = "none";
      });
      activeNavItem = null;
    }
  });

  // Add a function to ensure mega menu styles are properly applied
  const forceMegaMenuStyles = function () {
    if (megaMenu) {
      megaMenu.style.cssText = `
                position: absolute !important;
                top: 100% !important;
                left: 0 !important;
                right: 0 !important;
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                background-color: transparent !important;
                z-index: 40 !important;
                border-top: 1px solid #e5e7eb !important;
            `;

      menuContents.forEach((content) => {
        const menuContent = content.getAttribute("data-menu-content");

        // All menus use the same full width now
        content.style.cssText = `
                    width: 1488px !important;
                    max-width: 1488px !important;
                    margin: 0 auto !important;
                    padding: 2rem !important;
                    background-color: white !important;
                    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1) !important;
                `;

        // Special case for new-featured menu grid columns
        if (menuContent === "new-featured") {
          // Update grid columns for new-featured
          const categoryLists = content.querySelectorAll(
            ".DesktopSubNav_sub-menu-category-list",
          );
          categoryLists.forEach((list) => {
            list.style.cssText = `
                            list-style: none !important;
                            padding: 0 !important;
                            margin: 0 !important;
                            width: 100% !important;
                            display: grid !important;
                            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                            gap: 2rem !important;
                        `;
          });
        }

        // Style all Under Armour style elements
        const categoryLists = content.querySelectorAll(
          ".DesktopSubNav_sub-menu-category-list",
        );
        categoryLists.forEach((list) => {
          list.style.cssText = `
                        list-style: none !important;
                        padding: 0 !important;
                        margin: 0 !important;
                        width: 100% !important;
                        display: grid !important;
                        grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
                        gap: 2rem !important;
                    `;
        });

        // Style all banner containers
        const bannerContainers = content.querySelectorAll(
          ".b-navigation_banner-container",
        );
        bannerContainers.forEach((container) => {
          container.style.cssText = `
                        display: flex !important;
                        flex-direction: column !important;
                        height: 100% !important;
                    `;
        });

        // Style all banner images
        const bannerImages = content.querySelectorAll(
          ".b-navigation_banner-image",
        );
        bannerImages.forEach((image) => {
          image.style.cssText = `
                        width: 100% !important;
                        height: auto !important;
                        border-radius: 8px !important;
                        object-fit: cover !important;
                    `;
        });

        // Style all category titles
        const categoryTitles = content.querySelectorAll(
          ".DesktopSubNav_sub-menu-category-title",
        );
        categoryTitles.forEach((title) => {
          title.style.cssText = `
                        font-size: 14px !important;
                        font-weight: 600 !important;
                        text-transform: uppercase !important;
                        letter-spacing: 0.5px !important;
                        color: #111827 !important;
                        margin-bottom: 16px !important;
                        display: block !important;
                        text-decoration: none !important;
                    `;
        });

        // Style all category groupings
        const categoryGroupings = content.querySelectorAll(
          ".DesktopSubNav_sub-menu-category-grouping",
        );
        categoryGroupings.forEach((grouping) => {
          grouping.style.cssText = `
                        list-style: none !important;
                        padding: 0 !important;
                        margin: 0 !important;
                        display: flex !important;
                        flex-direction: column !important;
                        gap: 12px !important;
                    `;
        });
      });
    }
  };

  // Apply immediately
  forceMegaMenuStyles();

  // And also after a slight delay to ensure everything is loaded
  setTimeout(forceMegaMenuStyles, 500);

  // Apply again after a longer delay to handle any browser inconsistencies
  setTimeout(forceMegaMenuStyles, 1000);

  // Apply on window resize
  window.addEventListener("resize", forceMegaMenuStyles);
});

