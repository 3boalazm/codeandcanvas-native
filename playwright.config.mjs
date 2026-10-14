import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', timeout: 30000, fullyParallel: false, workers: 1, retries: 0,
  reporter: [['list'], ['json', { outputFile: 'test-results/results.json' }]],
  use: {
    baseURL: process.env.TEST_BASE_URL || 'http://127.0.0.1:3000',
    reducedMotion: 'reduce', viewport: { width: 1440, height: 900 },
    trace: 'retain-on-failure', screenshot: 'only-on-failure',
    launchOptions: process.env.PW_EXECUTABLE_PATH ? {
      executablePath: process.env.PW_EXECUTABLE_PATH,
      args: process.env.PW_BROWSER_ARGS ? JSON.parse(process.env.PW_BROWSER_ARGS) : ['--no-sandbox', '--disable-dev-shm-usage'],
    } : {},
  },
  webServer: {
    command: 'npm run dev', url: 'http://127.0.0.1:3000', reuseExistingServer: !process.env.CI,
  },
});
