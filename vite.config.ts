import { fileURLToPath, URL } from 'node:url'
import fs from 'node:fs'
import path from 'node:path'

import { defineConfig, type Connect, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

interface Release {
  date: string;
  changes: string[];
}

interface OtaDevice {
  codename: string;
  systems?: Array<{
    name: string;
    versions?: Array<{
      version: string;
      releases?: Release[];
    }>;
  }>;
}

const otaDir = fileURLToPath(new URL('./src/ota', import.meta.url));

const decodeHtmlEntities = (value: string): string => {
  return value
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
};

const stripHtml = (value: string): string => {
  return decodeHtmlEntities(value.replace(/<[^>]*>/g, '')).trim();
};

const loadOtaDevices = (): OtaDevice[] => {
  const files = fs.readdirSync(otaDir).filter((file) => file.endsWith('.json'));
  return files.map((file) => {
    const fullPath = path.join(otaDir, file);
    return JSON.parse(fs.readFileSync(fullPath, 'utf-8')) as OtaDevice;
  });
};

const otaDevices = loadOtaDevices();

const buildBpPlainText = (codename: string): string | null => {
  const device = otaDevices.find((item) => item.codename === codename);
  if (!device) return null;

  const aviumSystem = device.systems?.find((system) => system.name === 'AviumUI');
  const targetVersion = aviumSystem?.versions?.find((version) => version.version === 'avium-16');
  if (!targetVersion?.releases?.length) return null;

  const releases = [...targetVersion.releases].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  );

  return releases
    .map((release) => {
      const content = (release.changes || []).map((line) => stripHtml(line)).join('\n');
      return `==================\n${release.date}(时间)\n==================\n${content}`;
    })
    .join('\n\n');
};

const alwaysPlainTextPrefix = '/plain/device';

const parseAvium16DeviceFromPath = (pathname: string, prefix = '/device'): string | null => {
  const normalizedPrefix = prefix.split('/').filter(Boolean);
  const segments = pathname.split('/').filter(Boolean);
  const requiredLength = normalizedPrefix.length + 3;

  if (segments.length !== requiredLength) return null;

  for (let i = 0; i < normalizedPrefix.length; i += 1) {
    if (segments[i] !== normalizedPrefix[i]) return null;
  }

  const codenameIndex = normalizedPrefix.length;
  const systemIndex = codenameIndex + 1;
  const versionIndex = codenameIndex + 2;

  if (segments[systemIndex] !== 'AviumUI' || segments[versionIndex] !== 'avium-16') {
    return null;
  }

  return decodeURIComponent(segments[codenameIndex]);
};

const bpPlainTextMiddleware = (): Plugin => {
  const register = (middlewares: Connect.Server) => {
    middlewares.use((req, res, next) => {
      const userAgent = req.headers['user-agent'] || '';
      if (!userAgent.includes('Build/BP')) {
        next();
        return;
      }

      const pathname = new URL(req.url || '/', 'http://localhost').pathname;
      const codename = parseAvium16DeviceFromPath(pathname, '/device');
      
      if (!codename) {
        next();
        return;
      }

      const plainText = buildBpPlainText(codename);
      if (!plainText) {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'text/plain; charset=utf-8');
        res.end('未找到更新日志');
        return;
      }

      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.end(plainText);
    });
  };

  return {
    name: 'bp-plain-text-changelog',
    configureServer(server) {
      register(server.middlewares);
    },
    configurePreviewServer(server) {
      register(server.middlewares);
    },
  };
};

const alwaysPlainTextPagePlugin = (): Plugin => {
  const register = (middlewares: Connect.Server) => {
    middlewares.use((req, res, next) => {
      const pathname = new URL(req.url || '/', 'http://localhost').pathname;
      const codename = parseAvium16DeviceFromPath(pathname, alwaysPlainTextPrefix);
      if (!codename) {
        next();
        return;
      }

      const plainText = buildBpPlainText(codename);
      if (!plainText) {
        res.statusCode = 404;
        res.setHeader('Content-Type', 'text/plain; charset=utf-8');
        res.end('未找到更新日志');
        return;
      }

      res.statusCode = 200;
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.end(plainText);
    });
  };

  return {
    name: 'always-plain-text-page',
    configureServer(server) {
      register(server.middlewares);
    },
    configurePreviewServer(server) {
      register(server.middlewares);
    },
    generateBundle() {
      otaDevices.forEach((device) => {
        const content = buildBpPlainText(device.codename);
        if (!content) return;

        const fileName = `plain/device/${encodeURIComponent(device.codename)}/AviumUI/avium-16/index.txt`;
        this.emitFile({
          type: 'asset',
          fileName,
          source: content,
        });
      });
    },
  };
};

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    alwaysPlainTextPagePlugin(),
    bpPlainTextMiddleware(),
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('mdui-')
        }
      }
    }),
    vueJsx(),
    // vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
