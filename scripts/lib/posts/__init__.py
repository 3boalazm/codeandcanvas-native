# -*- coding: utf-8 -*-
"""Blog posts — literal copy of the live articles (English, as published).
Each module exports POST = dict(slug, title, title_ar, cat, cat_ar, minutes, date,
author ('cc'|'ma'), emoji, excerpt, excerpt_ar, stats, body, takeaways, faq, related)."""
from importlib import import_module

ORDER = ['p01_wrong_product', 'p02_idea_to_product', 'p03_software_alone', 'p04_digital_transformation_smes',
         'p05_product_thinking', 'p06_brands_feel_the_same', 'p07_brand_systems', 'p08_design_systems',
         'p09_creative_strategy_ai', 'p10_experience_design']


def all_posts():
    out = []
    for m in ORDER:
        try:
            out.append(import_module(f'posts.{m}').POST)
        except ModuleNotFoundError:
            pass
    return out
