/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.2s ease-in-out',
        'slide-up': 'slideUp 0.2s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
      },
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
    },
  },
  plugins: [
    // Custom variant for product tile hover states
    function({ addVariant }) {
      addVariant('product-hover', ['&:hover', '.group:hover &'])
    },
    // Plugin for aspect ratio support
    require('@tailwindcss/aspect-ratio'),
    // Plugin for forms
    require('@tailwindcss/forms'),
  ],
  variants: {
    extend: {
      opacity: ['group-hover'],
      transform: ['group-hover'],
      translate: ['group-hover'],
      scale: ['group-hover', 'hover'],
      backgroundColor: ['active', 'group-hover'],
      textColor: ['active', 'group-hover'],
    },
  },
} 
