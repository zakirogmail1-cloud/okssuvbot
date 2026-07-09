# -*- coding: utf-8 -*-
"""
Mahsulotlar katalogi.

Yangi mahsulot qo'shish yoki narx/minimalni o'zgartirish uchun shu ro'yxatni tahrirlang.
Har bir mahsulot:
  - id:      noyob kalit (o'zgartirmang, buyurtmalarda saqlanadi)
  - price:   narxi (so'mda, butun son) — bitta birlik uchun
  - min_qty: minimal buyurtma miqdori (shundan kam bo'lsa tanlab bo'lmaydi)
  - unit:    "dona" yoki "blok" (o'lchov birligi)
  - emoji:   chiroyli ko'rinish uchun belgi
  - name:    3 tilda nomi (uz / ru / en)
"""

import json

PRODUCTS = [
    {
        "id": "19l", "price": 10000, "min_qty": 1, "unit": "dona", "emoji": "💧",
        "name": {"uz": "19 litr", "ru": "19 литров", "en": "19 liters"},
    },
    {
        "id": "12l", "price": 8500, "min_qty": 3, "unit": "dona", "emoji": "💧",
        "name": {"uz": "12 litr", "ru": "12 литров", "en": "12 liters"},
    },
    {
        "id": "6l", "price": 5500, "min_qty": 5, "unit": "dona", "emoji": "💦",
        "name": {"uz": "6 litr", "ru": "6 литров", "en": "6 liters"},
    },
    {
        "id": "05l", "price": 15400, "min_qty": 5, "unit": "blok", "emoji": "🥤",
        "name": {"uz": "0.5 litr", "ru": "0.5 литра", "en": "0.5 L"},
    },
    {
        "id": "1l", "price": 14400, "min_qty": 5, "unit": "blok", "emoji": "🥤",
        "name": {"uz": "1 litr", "ru": "1 литр", "en": "1 L"},
    },
    {
        "id": "15l", "price": 13200, "min_qty": 5, "unit": "blok", "emoji": "🥤",
        "name": {"uz": "1.5 litr", "ru": "1.5 литра", "en": "1.5 L"},
    },
]

MAX_QTY = 99

# O'lchov birliklari tarjimasi
UNIT_LABELS = {
    "dona": {"uz": "dona", "ru": "шт", "en": "pcs"},
    "blok": {"uz": "blok", "ru": "блок", "en": "block"},
}


def get_product(product_id: str):
    """id bo'yicha mahsulotni topish (topilmasa None)."""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None


def product_name(product_id: str, lang: str = "uz") -> str:
    p = get_product(product_id)
    if not p:
        return product_id
    return p["name"].get(lang, p["name"].get("uz", product_id))


def product_price(product_id: str) -> int:
    p = get_product(product_id)
    return p["price"] if p else 0


def product_min_qty(product_id: str) -> int:
    p = get_product(product_id)
    return p.get("min_qty", 1) if p else 1


def product_unit(product_id: str) -> str:
    p = get_product(product_id)
    return p.get("unit", "dona") if p else "dona"


def unit_label(unit: str, lang: str = "uz") -> str:
    return UNIT_LABELS.get(unit, {}).get(lang, unit)


def step_qty(product_id: str, current: int, delta: int) -> int:
    """
    ➕ / ➖ bosilganда yangi sonni hisoblaydi (minimal buyurtma mantiqi bilan).
    - 0 dan ➕ bosilса → minimal miqdorга sakraydi
    - minimal miqdorда ➖ bosilса → 0 ga tushadi (buyurtmadan chiqarish)
    - aks holda ±1 (0..MAX_QTY oralig'ida)
    """
    mn = product_min_qty(product_id)
    cur = int(current or 0)
    if delta > 0:
        if cur <= 0:
            return mn
        return min(cur + 1, MAX_QTY)
    else:
        if cur <= mn:
            return 0
        return cur - 1


# ─── Buyurtma itemlari (JSON) ───

def build_items(cart: dict) -> list:
    """cart = {product_id: qty} dan buyurtma itemlari ro'yxatini yasaydi (qty > 0)."""
    items = []
    for pid, qty in cart.items():
        if qty and qty > 0:
            p = get_product(pid)
            if not p:
                continue
            items.append({
                "id": pid,
                "name": p["name"]["uz"],
                "qty": int(qty),
                "price": int(p["price"]),
                "unit": p.get("unit", "dona"),
            })
    return items


def items_to_json(items: list) -> str:
    return json.dumps(items, ensure_ascii=False)


def items_from_json(items_json) -> list:
    if not items_json:
        return []
    if isinstance(items_json, list):
        return items_json
    try:
        return json.loads(items_json)
    except Exception:
        return []


def items_total(items: list) -> int:
    return sum(int(i.get("qty", 0)) * int(i.get("price", 0)) for i in items)


def items_count(items: list) -> int:
    return sum(int(i.get("qty", 0)) for i in items)


def format_items_lines(items: list, lang: str = "uz") -> str:
    """Har bir mahsulotni chiroyli qatorlarga formatlaydi."""
    lines = []
    for i in items:
        name = product_name(i.get("id", ""), lang) or i.get("name", "")
        qty = int(i.get("qty", 0))
        price = int(i.get("price", 0))
        unit = unit_label(i.get("unit", "dona"), lang)
        sub = qty * price
        lines.append(f"💧 {name} × {qty} {unit} = {sub:,} so'm")
    return "\n".join(lines)
