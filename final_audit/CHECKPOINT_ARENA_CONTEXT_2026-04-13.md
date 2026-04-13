# CHECKPOINT — Neural-Arithmetic-Diagnostics (Arena Context)
**تاريخ:** 2026-04-13  
**الريبو:** `ultramind21/Neural-Arithmetic-Diagnostics`  
**الفرع الافتراضي على GitHub:** `main` (origin/HEAD → origin/main)  
**فلسفة النظام:** Evidence-first. Project 12 هو **Claim Authority Layer**.

---

## 0) ما الذي تم إغلاقه؟

### A) P0 (Stability fixes) — أُغلِق
أصلحنا نقاط حرجة في `src/` بدون كسر validation.

**P0 fixes الأساسية:**
- `src/env/soroban_env.py`: إضافة guard لـ **unknown action** → illegal + terminate.
- `src/env/encode.py`: جعل encode يعتمد على `_obs()` بدون افتراض feature count ثابت.
- `src/teacher/dataset_gen.py`: منع silent skipping → **fail-fast** عند أخطاء dataset generation.
- توحيد/تصحيح docstrings حول observation shape لتطابق الواقع.

**Commit مهم:**
- `8473f19` — P0: guard unknown actions + obs encoding shape-agnostic + fail-fast dataset (كان على فرع P0 ثم دُمج لاحقًا إلى main).

---

### B) Platform P0 (Packaging + CI + "one command verify") — أُغلِق
حوّلنا الريبو إلى "toolkit قابل للتشغيل" بدون لمس طبقة الأبحاث.

**أُضيف:**
- `pyproject.toml` لنشر package.
- package جديد: `nad/` + CLI:
  - `nad-check-links`
  - `nad-diff-gate`
- `pytest.ini` لتقييد اكتشاف الاختبارات إلى `tests/` وتجاهل `archive_optional/`.
- `tests/test_pytest_smoke.py` wrappers لتشغيل `run_tests()` تحت pytest.
- `CONTRIBUTING.md`
- `project_12/docs/CLAIM_AUTHORITY.md`
- GitHub Actions CI: `.github/workflows/ci.yml`
- "ONE command verify": `tools/verify_platform_p0.py`

**Tag milestone (ليس release):**
- `platform-p0-2026-04-11` → يشير إلى commit `8c9c07d` (Platform P0 snapshot).

**Platform P0 دُمج في main** عبر merge commits سابقة (موثقة في التاريخ).

---

### C) Sprint P1 (Repro Hardening + Docs + CI matrix) — أُغلِق ومُدمج في main
رفعنا الـreproducibility عمليًا:
- `requirements.lock.txt` (ledger مولّد من clean venv من `requirements.txt`).
- `tools/verify_platform_p0.py` صار يكتب reports محلية (gitignored):
  - `tools/verify_reports/pip_freeze.txt`
  - `tools/verify_reports/platform_p0_report.json`
- أضفنا hashing ledgers للـauthority layer:
  - `project_12/results/_hashes/p12_docs_sha256.json`
  - `project_12/results/_hashes/p12_results_sha256.json`
- أضفنا `tools/hash_tree.py` (sha256 tree hash generator) ويتجاهل `_hashes/` لتجنب self-reference.
- CI صار **matrix**: `ubuntu-latest` + `windows-latest`.
- أضفنا توثيق reproducibility:
  - `docs/REPRODUCIBILITY.md`
  - تحديث `README.md` + `CONTRIBUTING.md`.

**إصلاح CI على Windows:**
- سبب الفشل كان encoding بسبب emojis (مثل `✅`) في مخرجات `tests/test_env.py`, `tests/test_rules.py`, `tests/test_teacher.py`.
- تم استبدال emojis بـASCII مثل `[OK]` لضمان التوافق مع Windows runner.

**PR الدمج:**
- PR #1 تم دمجه إلى `main` بــ merge commit:
  - `089464d...` — "Merge pull request #1 from ultramind21/sprint-p1-repro-hardening"
- CI على main بعد الدمج: **success** (ubuntu + windows).

**Commits بارزة ضمن P1:**
- `bee4fcd` — إضافة `requirements.lock.txt` + تحديث `.gitignore`.
- `3a935eb` — P1 tooling + docs + CI matrix + hash ledgers + verify reports.
- `1eed548`, `f84b341`, `2c73b1e` — تنظيف emojis في اختبارات لضمان Windows CI.
- `089464d...` — merge PR #1 إلى main.

---

## 1) ما هي "السلطة" على claims؟
- **Project 12 هو Claim Authority**: أي claim "publishable" يجب أن يمر عبر `project_12/` artifacts + gates + snapshots.
- ملف السياسة: `project_12/docs/CLAIM_AUTHORITY.md`.

---

## 2) كيف أتحقق من أن كل شيء OK؟ (أوامر معيارية)

### A) One-command verification (المعيار)
```bash
python tools/verify_platform_p0.py
```
يعمل:
1) compile (`src/` + `nad/`)
2) pytest smoke gate (wrappers)
3) legacy tests:
   - `python tests/test_env.py`
   - `python tests/test_rules.py`
   - `python tests/test_teacher.py`
4) `nad-check-links project_12/docs`
5) `nad-diff-gate` self-test

### B) pytest (سريع)
```bash
python -m pytest -q
```

### C) hash ledgers (authority integrity)
```bash
python tools/hash_tree.py project_12/docs > project_12/results/_hashes/p12_docs_sha256.json
python tools/hash_tree.py project_12/results > project_12/results/_hashes/p12_results_sha256.json
```

---

## 3) CI (GitHub Actions)
المسار: `.github/workflows/ci.yml`  
يشغّل على:
- Ubuntu
- Windows

ويشمل:
- install deps
- compile
- pytest
- CLI smoke
- `python tools/verify_platform_p0.py`
- large file guard (20MB)  
  (تم إصلاح خطوة large file guard بإضافة `shell: bash` لتعمل على Windows.)

---

## 4) ما الذي **ليس** "freeze علمي" رغم أنه reproducible؟
هذه نقطة مفصلية:
- ما لدينا الآن = **Engineering milestone** + "deterministic-ish verify" + CI.
- ليس لدينا بعد:
  - dependency hash lock حقيقي (pip-tools/uv lock hashes)
  - branch protection rules + required checks enforced
  - signed tags/commits
  - release tag `v0.1.0` رسمي + release notes

تم توضيح ذلك داخل: `docs/REPRODUCIBILITY.md`.

---

## 5) ملاحظات تشغيل مهمّة
- `requirements.lock.txt` هو **ledger** ناتج عن clean venv من `requirements.txt`.  
  الهدف: audit trail. ليس ضمان universal cross-OS/CUDA (خصوصًا Torch).
- `tools/verify_reports/` **gitignored** عمدًا لتجنب churn.
- تم إزالة/منع ملفات debug المؤقتة عدة مرات لأنّها تفسد traceability.

---

## 6) أين وصلنا "عمليةً" وما التالي؟

### الحالة الحالية
- `main` يحتوي: P0 + Platform P0 + P1 (تم الدمج).
- PR #1 مغلق ومندمج.
- CI على main ناجح (Ubuntu + Windows).

### Sprint P2 (المقترح التالي)
**هدفه: رفع "Reproducibility" من ledger إلى lock حقيقي + governance.**
- Dependency hash-lock:
  - خيار 1: `pip-tools` (`pip-compile --generate-hashes`)
  - خيار 2: `uv lock` (أسرع وحديث)
- Branch protections:
  - require CI checks
  - منع direct pushes على main
- Release engineering:
  - tag `v0.1.0` (أو `v0.1.0-alpha`) + changelog مختصر
- (اختياري) CI على macOS لاحقًا.

---

## 7) بروتوكول التعامل مع "الوكيل" (قاعدة تشغيل)
- أي تغيير = minimal diff + evidence (git diff + gates).
- ممنوع scripts مؤقتة داخل الريبو.
- ممنوع snippets كأداة تنفيذ (تسببت في انحرافات وcommits على فروع خاطئة سابقًا).
- قبل أي merge: إثبات checks + run IDs من GitHub Actions أو `gh`.

---

## 8) آخر عمليات موثقة
- **2026-04-13 20:58:32 UTC**: PR #1 دُمج إلى main بنجاح.
- **2026-04-13 20:58:35 UTC**: CI على main تم تشغيله، النتيجة **success**.
- **Branch sprint-p1-repro-hardening**: تم حذفه بعد الدمج (كما هو متوقع).

---

**Last Updated:** 2026-04-13 20:58 UTC  
**Status:** ✅ Sprint P1 CLOSED, Ready for P2
