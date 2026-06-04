/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#00AEEF',
          light: '#33BEF2',
        },
        secondary: {
          DEFAULT: '#0033A0',
        },
        accent: {
          DEFAULT: '#f0c200',
        },
        'bg-light': '#FFFFFF',
        'text-dark': '#333333',
      },
      backgroundImage: {
        'grad-primary': 'linear-gradient(135deg, #00AEEF 0%, #0033A0 100%)',
      },
      boxShadow: {
        '3xl': '0 32px 64px -12px rgba(0, 0, 0, 0.5)',
      }
    },
  },
  plugins: [],
}
