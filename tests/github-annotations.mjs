/* Playwright reporter that republishes each failing test as a GitHub Actions
   error annotation.

   Why: the gate's Playwright step is the only place the browser matrix really
   runs, and when it fails the useful text (which assertion, which route, which
   breakpoint) lives in the job log. Annotations are retrievable through the
   public check-runs API, so they make a red gate diagnosable from outside CI
   without downloading logs or artifacts.

   Only active under GitHub Actions (`GITHUB_ACTIONS`), so local runs keep their
   normal list/json output. */

const esc = (s) => String(s)
  .replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A');

export default class GithubAnnotations {
  constructor() { this.failures = []; }

  onBegin() { this.failures = []; }

  onTestEnd(test, result) {
    if (result.status === 'passed' || result.status === 'skipped') return;
    const file = test.location?.file || 'tests';
    const line = test.location?.line || 1;
    const message = (result.error?.message || result.status || 'failed')
      .replace(/\u001b\[[0-9;]*m/g, '')   // strip ANSI colours
      .split('\n').slice(0, 12).join('\n') // keep the annotation readable
      .replace(/\*\//g, '*\\/');         // never close a JS block comment
    const row = {
      file: file.replace(/^.*\/(tests\/)/, '$1'),
      line,
      title: `Playwright: ${test.titlePath().filter(Boolean).slice(1).join(' › ')}`,
      message,
      snippet: result.error?.snippet ? `at ${result.error.snippet}` : '',
    };
    this.failures.push(row);
    const body = `${row.title}\n${message}${row.snippet ? `\n${row.snippet}` : ''}`;
    process.stdout.write(`::error file=${row.file},line=${row.line},title=${esc(row.title)}::${esc(body)}\n`);
  }

  onEnd(result) {
    const failed = this.failures.length;
    const summary = `Playwright: ${failed} failing test(s), overall status ${result.status}`;
    process.stdout.write(`::notice title=Playwright summary::${esc(summary)}\n`);
    for (const f of this.failures) process.stdout.write(`  · ${f.file}:${f.line} ${f.title}\n`);
  }

  printsToStdio() { return false; }
}
