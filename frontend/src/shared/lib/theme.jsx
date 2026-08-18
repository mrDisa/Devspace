import { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext(null);

function readInitialTheme() {
  const stored = localStorage.getItem('theme');
  if (stored === 'light' || stored === 'dark') return stored === 'dark';
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? true;
}

// Applied once at the root of the app (see main.jsx) so the chosen theme is
// active on every screen, including /login and /signup, instead of only
// inside the authenticated layout.
export function ThemeProvider({ children }) {
  const [dark, setDark] = useState(readInitialTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  }, [dark]);

  return (
    <ThemeContext.Provider value={{ dark, toggle: () => setDark((value) => !value), setDark }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
