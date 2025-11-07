/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.{html,js}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'serif': ['Merriweather', 'Georgia', 'serif'],
      },
      colors: {
        'theme-light': '#ffffff',
        'theme-dark': '#1a1a1a',
        'theme-medium': '#f5f5f5',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}