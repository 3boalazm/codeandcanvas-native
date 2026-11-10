import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', timeout: 30000, fullyParallel: false, workers: 1, retries: 0,
  reporter: [
    ['list'],
    ['json', { outputFile: 'test-results/results.json' }],
    // Inside GitHub Actions, republish every failure as an error annotation so
    // a red gate can be diagnosed from the check-runs API alone (job logs are
    // not always retrievable). No effect locally.
    ...(process.env.GITHUB_ACTIONS ? [['./tests/github-annotations.mjs']] : []),
  ],
  use: {
    baseURL: process.env.TEST_BASE_URL || 'http://127.0.0.1:3000',
    reducedMotion: 'reduce', viewport: { width: 1440, height: 900 },
    // The app shell caches responses, which would make ordinary E2E assertions
    // non-deterministic. tests/pwa.spec.mjs opts back in for its own worker tests.
    serviceWorkers: 'block',
    trace: 'retain-on-failure', screenshot: 'only-on-failure',
    launchOptions: process.env.PW_EXECUTABLE_PATH ? {
      executablePath: process.env.PW_EXECUTABLE_PATH,
      args: process.env.PW_BROWSER_ARGS ? JSON.parse(process.env.PW_BROWSER_ARGS) : ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
      ...(process.env.PW_LD_LIBRARY_PATH ? { env: { ...process.env, LD_LIBRARY_PATH: process.env.PW_LD_LIBRARY_PATH } } : {}),
    } : {},
  },
  webServer: {
    command: 'npm run dev', url: 'http://127.0.0.1:3000', reuseExistingServer: !process.env.CI,
  },
});
