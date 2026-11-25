/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: {
          bg: '#F7F6F2',
          surface: '#FFFFFF',
          stone: '#ECEAE3',
          border: '#8A8478',
          divider: '#D5D0C5',
          ink: '#14181F',
          slate: '#4A5260',
        },
        night: {
          bg: '#0B0F17',
          surface: '#151C28',
          elevated: '#1E293B',
          border: '#64748B',
          divider: '#2B3547',
          ink: '#F8FAFC',
          slate: '#CBD5E1',
        },
        cobalt: {
          DEFAULT: '#1D4ED8',
          hover: '#1E40AF',
          light: '#60A5FA',
          soft: '#EBF1FC',
        },
      },
      fontFamily: {
        display: ['"Bahnschrift"', '"Segoe UI"', 'system-ui', 'sans-serif'],
        sans: ['"Segoe UI"', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"Consolas"', '"Cascadia Code"', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
};
