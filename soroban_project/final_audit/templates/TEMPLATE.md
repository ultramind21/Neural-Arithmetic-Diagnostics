# 🔍 CODE AUDIT REPORT TEMPLATE

**File:** `[FILENAME]`  
**Project:** `[PROJECT 1 / 2 / 3]`  
**Date:** [DATE]  
**Auditor:** [AUTO]  

---

## 📝 FILE SUMMARY
- **Lines of Code:** [COUNT]
- **Purpose:** [BRIEF]
- **Key Variables:** [LIST]
- **Key Functions:** [LIST]

---

## 🔎 AUDIT CHECKLIST

### 1️⃣ LOGIC & CORRECTNESS
- [ ] No off-by-one errors
- [ ] Arithmetic operations correct
- [ ] Loop conditions sound
- [ ] Data flow clear
- [ ] No unreachable code
- [ ] Return values correct

**Issues Found:**
```
- [Issue 1 if any]
- [Issue 2 if any]
```

**Severity:** ⚠️ CRITICAL / 🟡 MINOR / ✅ NONE

---

### 2️⃣ DATA HANDLING
- [ ] No hardcoded values (except config)
- [ ] Variables properly initialized
- [ ] No unintended side effects
- [ ] Proper error handling
- [ ] No NaN/Inf creation

**Issues Found:**
```
- [Issue 1 if any]
```

**Severity:** ⚠️ CRITICAL / 🟡 MINOR / ✅ NONE

---

### 3️⃣ FLOATING POINT ISSUES
- [ ] No suspicious rounding
- [ ] No accumulation errors
- [ ] Division by zero prevented
- [ ] Type conversions explicit

**Issues Found:**
```
- [Issue 1 if any]
```

**Severity:** ⚠️ CRITICAL / 🟡 MINOR / ✅ NONE

---

### 4️⃣ CODE QUALITY
- [ ] Well-commented
- [ ] Clear variable names
- [ ] Logical organization
- [ ] No dead code

**Issues Found:**
```
- [Issue 1 if any]
```

**Severity:** ⚠️ CRITICAL / 🟡 MINOR / ✅ NONE

---

### 5️⃣ DEPENDENCIES & IMPORTS
- [ ] All imports used
- [ ] No conflicting libraries
- [ ] Version compatibility clear
- [ ] External functions clearly called

**Issues Found:**
```
- [Issue 1 if any]
```

**Severity:** ⚠️ CRITICAL / 🟡 MINOR / ✅ NONE

---

## 📊 OVERALL ASSESSMENT

**Code Quality:** ✅ CLEAN / 🟡 ACCEPTABLE / ⚠️ ISSUES  

**Critical Issues:** [0 / 1 / 2+]  
**Minor Issues:** [0 / 1 / 2+]  

**Recommendation:**
```
✅ PASS - Safe to use
🟡 PASS WITH NOTES - Document issues
⚠️ FAIL - Requires revision
```

---

## 🔗 LINKED FILES
- Logical Validation Report: `LOGICAL_VALIDATION_[FILENAME].md`
- Data Integrity Log: `DATA_INTEGRITY_[FILENAME].md`
- Reproduction Results: `REPRODUCTION_[FILENAME].md`

---

**Code Audit Status:** [PENDING / IN PROGRESS / COMPLETE]  
**Last Updated:** [DATE]
