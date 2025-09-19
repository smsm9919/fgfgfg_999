# FlowMarket — Render Blueprint (100% Ready)

نشر فوري على Render باسم خدمة **flow-market** ودومين تلقائي:
`https://flow-market.onrender.com`

## ما الذي ستحصل عليه؟
- Flask + Gunicorn إعداد إنتاجي.
- PostgreSQL (Free) تلقائي عبر `render.yaml`.
- Health checks: `/healthz` و `/db-ping`.
- **رفع صور ImgBB** عبر `/upload` (Auto-Register).
- **مصادقة جاهزة** `/auth/login` و `/auth/logout` و `/auth/health` (Auto-Register).
- يعمل حتى لو ما عدّلتش ولا سطر.

## النشر (3 خطوات)
1) ارفع هذا المجلد إلى GitHub (جذر الريبو لازم يحتوي `render.yaml`).
2) Render → **New → Blueprint** → اختر الريبو.
3) أضف متغير بيئة:
   - `IMGBB_API_KEY = <ضع مفتاح ImgBB>`

## تحقق بعد النشر
- GET `/healthz` → `{ok: true}`
- GET `/db-ping` → `{ok: true, result: 1}`
- POST `/upload` (form-data: file) → يرجّع رابط ImgBB.
- POST `/auth/login` → يرجّع JSON واضح دائمًا (بدون كراش).

> **ملاحظة**: ملفّات `imgbb_auto.py` و `auth_auto.py` تسجّل نفسها تلقائيًا، فقط تأكد أنها في جذر المشروع.