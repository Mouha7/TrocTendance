/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'black': '#000000',
        'white': '#FFFFFF',
        'gray-light': '#F5F5F5',
        'gray-medium': '#A9A9A9',
        'gray-dark': '#333333',
      },
    },
  },
  plugins: [],
}

