/* /system/ only: copy a design-token value without any library or network call.
   The page uses native details/summary for the gallery, so no scroll listener,
   observer or animation is needed here. */
(() => {
  const buttons = document.querySelectorAll('.sys-token__copy');
  const status = document.getElementById('sys-copy-status');
  if (!buttons.length || !status) return;
  let clear;
  const isAr = () => document.documentElement.lang === 'ar';

  // A clipboard promise can stay pending in locked-down browsers; never leave
  // the live region empty, and fall back to a synchronous selection copy.
  async function copy(value) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await Promise.race([
          navigator.clipboard.writeText(value),
          new Promise((_, reject) => setTimeout(() => reject(new Error('clipboard timeout')), 1200)),
        ]);
        return true;
      } catch (_) { /* try the legacy path below */ }
    }
    try {
      const field = document.createElement('textarea');
      field.value = value;
      field.setAttribute('readonly', '');
      field.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
      document.body.appendChild(field);
      field.select();
      const ok = document.execCommand('copy');
      field.remove();
      return ok;
    } catch (_) {
      return false;
    }
  }

  buttons.forEach((button) => button.addEventListener('click', async () => {
    const value = button.getAttribute('data-copy') || '';
    const ok = await copy(value);
    status.textContent = ok
      ? `${isAr() ? 'تم النسخ' : 'Copied'} ${value}`
      : (isAr() ? 'تعذّر النسخ — حدّد القيمة يدويًا' : 'Copy unavailable — select the value manually');
    clearTimeout(clear);
    clear = setTimeout(() => { status.textContent = ''; }, 3500);
  }));
})();
