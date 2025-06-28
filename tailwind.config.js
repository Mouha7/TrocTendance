/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Couleurs inspirées du logo flamme
        'flame': {
          50: '#FFF8F0',   // très clair
          100: '#FFEDD5',  // clair
          200: '#FED7AA',  // 
          300: '#FDBA74',  // 
          400: '#FB923C',  // 
          500: '#F97316',  // orange principal
          600: '#EA580C',  // orange foncé
          700: '#C2410C',  // rouge-orange
          800: '#9A3412',  // rouge foncé
          900: '#7C2D12',  // très foncé
        },
        'primary': '#F97316',    // Orange principal
        'secondary': '#EA580C',  // Orange foncé
        'accent': '#C2410C',     // Rouge-orange
        'dark': '#7C2D12',       // Très foncé
      }
    },
  },
  plugins: [],
}

