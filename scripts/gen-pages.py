# -*- coding: utf-8 -*-
"""Scaffolds the inner pages of codeandcanvas.net as static HTML.

    python3 scripts/gen-pages.py && node scripts/sync-chrome.mjs

The committed HTML files are the deliverable; this script only exists so the
repeated structures (service cards, closings, breadcrumbs) stay consistent.
Copy is the live WordPress copy (English) with Arabic twins in data-ar.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
from catalog import SERVICES, TRACKS, href  # noqa: E402
from h import esc, t, th, icon, arrow, svc_card, svc_grid, crumbs, closing, btn, page  # noqa: E402

import pages_services  # noqa: E402

BUILDERS = [pages_services.build]

if __name__ == '__main__':
    for b in BUILDERS:
        for out in b():
            print('wrote', os.path.relpath(out))
