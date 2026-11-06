import { ref, watchEffect } from 'vue';
import { hexFromArgb, sourceColorFromImage } from '@material/material-color-utilities';
import { wallpaperConfig } from './site';

export type ThemeMode = 'auto' | 'light' | 'dark';

const MODE_STORAGE_KEY = 'theme-mode';
const COLOR_STORAGE_KEY = 'ota-theme-color';
const DEFAULT_COLOR = '#6750A4';
const MODES: ThemeMode[] = ['auto', 'light', 'dark'];
const IMAGE_TIMEOUT = 8000;

interface CachedColor {
  date: string;
  color: string;
}

export const themeColor = ref(DEFAULT_COLOR);
export const themeMode = ref<ThemeMode>('auto');

const isThemeMode = (value: unknown): value is ThemeMode =>
  MODES.includes(value as ThemeMode);

const localDate = (): string => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
};

const readCachedColor = (): CachedColor | null => {
  try {
    const raw = localStorage.getItem(COLOR_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<CachedColor>;
    if (typeof parsed.color !== 'string' || !/^#[0-9a-f]{6}$/i.test(parsed.color)) return null;
    return { date: typeof parsed.date === 'string' ? parsed.date : '', color: parsed.color };
  } catch {
    return null;
  }
};

const writeCachedColor = (color: string) => {
  try {
    localStorage.setItem(COLOR_STORAGE_KEY, JSON.stringify({ date: localDate(), color } satisfies CachedColor));
  } catch {
    // Storage can be unavailable (private mode, quota); the in-memory color still applies.
  }
};

const loadImage = (src: string): Promise<HTMLImageElement> => {
  const { promise, resolve, reject } = Promise.withResolvers<HTMLImageElement>();
  const image = new Image();
  image.crossOrigin = 'anonymous';
  const timer = window.setTimeout(() => reject(new Error('Wallpaper request timed out')), IMAGE_TIMEOUT);
  image.onload = () => {
    window.clearTimeout(timer);
    resolve(image);
  };
  image.onerror = () => {
    window.clearTimeout(timer);
    reject(new Error('Wallpaper image failed to load'));
  };
  image.src = src;
  return promise;
};

const refreshColor = async () => {
  if (!wallpaperConfig.api) return;
  try {
    const image = await loadImage(wallpaperConfig.api);
    const color = hexFromArgb(await sourceColorFromImage(image));
    themeColor.value = color;
    writeCachedColor(color);
  } catch (error) {
    console.warn('Dynamic color initialization failed:', error);
  }
};

const applyToHost = () => {
  const host = document.getElementById('app');
  if (!host) return;
  host.setAttribute('color', themeColor.value);
  host.setAttribute('scheme', themeMode.value);
};

export const initTheme = () => {
  try {
    const saved = localStorage.getItem(MODE_STORAGE_KEY);
    if (isThemeMode(saved)) themeMode.value = saved;
  } catch {
    // Ignore unavailable storage.
  }

  const cached = readCachedColor();
  if (cached) themeColor.value = cached.color;

  watchEffect(applyToHost);

  if (!cached || cached.date !== localDate()) {
    void refreshColor();
  }
};

export const cycleThemeMode = () => {
  themeMode.value = themeMode.value === 'auto' ? 'light' : themeMode.value === 'light' ? 'dark' : 'auto';
  try {
    localStorage.setItem(MODE_STORAGE_KEY, themeMode.value);
  } catch {
    // Ignore unavailable storage.
  }
};
