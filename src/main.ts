import './assets/main.css';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import '@fontsource/noto-sans-sc/400.css';
import '@fontsource/noto-sans-sc/500.css';
import '@fontsource/noto-sans-sc/700.css';
import '@fontsource-variable/material-symbols-rounded/full.css';

import '@material/web/all.js';
import { themeFromSourceColor, applyTheme, argbFromHex, SchemeTonalSpot, Hct, hexFromArgb } from '@material/material-color-utilities';

function setExtraTokens(source: number, dark: boolean) {
  const scheme = new SchemeTonalSpot(Hct.fromInt(source), dark, 0.0);
  const extras: Record<string, number> = {
    'surface-dim': scheme.surfaceDim,
    'surface-bright': scheme.surfaceBright,
    'surface-container-lowest': scheme.surfaceContainerLowest,
    'surface-container-low': scheme.surfaceContainerLow,
    'surface-container': scheme.surfaceContainer,
    'surface-container-high': scheme.surfaceContainerHigh,
    'surface-container-highest': scheme.surfaceContainerHighest,
    'outline-variant': scheme.outlineVariant,
  };
  for (const [key, value] of Object.entries(extras)) {
    const token = `--md-sys-color-${key}`;
    const color = hexFromArgb(value);
    document.body.style.setProperty(token, color);
  }
}

// Apply Material 3 baseline theme immediately (before wallpaper loads)
const baselineTheme = themeFromSourceColor(argbFromHex('#6750A4'));
const savedMode = localStorage.getItem('theme-mode') as 'auto' | 'light' | 'dark' | null;
type ThemeMode = 'auto' | 'light' | 'dark';
function initIsDark(mode: ThemeMode): boolean {
  return mode === 'dark' || (mode === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
}
const initialMode: ThemeMode = (savedMode && ['auto', 'light', 'dark'].includes(savedMode)) ? savedMode : 'auto';
const initialDark = initIsDark(initialMode);
applyTheme(baselineTheme, { dark: initialDark, brightnessSuffix: true });
document.body.classList.toggle('dark', initialDark);
setExtraTokens(baselineTheme.source, initialDark);

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(router)

app.mount('#app')
