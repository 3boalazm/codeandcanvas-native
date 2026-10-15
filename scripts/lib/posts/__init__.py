# -*- coding: utf-8 -*-
"""Blog posts — literal copy of the live articles (English, as published).
Each module exports POST = dict(slug, title, title_ar, cat, cat_ar, minutes, date,
author ('cc'|'ma'), emoji, excerpt, excerpt_ar, stats, body, takeaways, faq, related).

`posts/ar/<same module>.py` carries the committed Arabic translation of one article as
AR = dict(body=…, side=…): the main column and the sidebar of `/ar/blog/<slug>/`, written
in the same markup as the English original so the shared CSS applies unchanged. It is
merged into POST['ar'] here; scripts/lib/pages_blog.py emits it as a build-time swap and
scripts/lib/arize.mjs performs the swap when it writes the Arabic twin.
"""
from importlib import import_module

ORDER = ['p01_wrong_product', 'p02_idea_to_product', 'p03_software_alone', 'p04_digital_transformation_smes',
         'p05_product_thinking', 'p06_brands_feel_the_same', 'p07_brand_systems', 'p08_design_systems',
         'p09_creative_strategy_ai', 'p10_experience_design']


def all_posts():
    out = []
    for m in ORDER:
        try:
            post = import_module(f'posts.{m}').POST
        except ModuleNotFoundError:
            continue
        try:
            post['ar'] = import_module(f'posts.ar.{m}').AR
        except ModuleNotFoundError:
            pass
        out.append(post)
    return out
