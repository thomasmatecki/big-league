module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "../api/iframes/templates/*.html"
  ],
  plugins: [],
  important: true,
  theme: {
    fontFamily: {
      display: ['Gilroy', 'sans-serif'],
      body: ['Graphik', 'sans-serif'],
    },
    extend: {
      colors: {
        cyan: '#9cdbff',
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      }
    }
  },
  variants: {
    opacity: ['responsive', 'hover']
  }
}
