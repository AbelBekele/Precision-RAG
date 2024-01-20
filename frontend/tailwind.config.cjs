/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      screens: {
        xs: "480px",
      },
      fontFamily: {
        inter: ["Inter var", "sans-serif"],
      },
      boxShadow: {
        card: "0 0 1px 0 rgba(0,0,0,0.06),0 10px 16px -1px rgba(0,0,0,0.2)",
        cardhover:
          "0 0 1px 0 rgba(0,0,0,0.06),0 10px 16px -1px rgba(0,0,0,0.2),0 0 0 3px rgba(0,0,0,0.1)",
      },
      colors: {
        black: "#040404",
        dark: "#000400",
        hero: "#000609",
        darkgrey: "#121415",
        accent: "#C5B358",
        brand: "#FF6347",
        text: "#f5f5f5",
        grey: "#e5e5e5",
      },
    },
  },
  plugins: [],
};
