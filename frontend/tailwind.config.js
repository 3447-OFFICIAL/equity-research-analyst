/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172026",
        line: "#d7dde2",
        accent: "#0f766e",
        signal: "#b45309",
      },
    },
  },
  plugins: [],
};
