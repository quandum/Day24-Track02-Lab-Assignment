# Kế Hoạch Thực Thi Chi Tiết — MedViet Data Governance Lab

**Học viên:** Trần Mạnh Chánh Quân  
**Mã học viên:** 2A202600786  
**Khóa học:** AICB-P2T2 · Lab #24 Extended  
**Thời gian dự kiến:** 3–4 giờ

---

## Tổng Quan

Xây dựng data governance pipeline end-to-end cho **MedViet** — startup y tế Việt Nam — đáp ứng chuẩn NĐ13/ISO 27001.

### Công Nghệ Sử Dụng

| Trụ cột | Công nghệ | Phần |
|---------|-----------|------|
| Phát hiện & ẩn danh PII | Microsoft Presidio + spaCy | Phần 2 |
| Kiểm soát truy cập | Casbin RBAC + FastAPI | Phần 3 |
| Mã hóa dữ liệu | AES-256-GCM envelope encryption | Phần 4 |
| Chất lượng dữ liệu | Great Expectations | Phần 5 |
| Security scanning | git-secrets, Bandit, TruffleHog | Phần 6 |
| OPA Policy | Rego language | Phần 7 |
| Compliance | NĐ13/2023 Checklist | Phần 8 |

---

---

## Phân Tích Yêu Cầu data-governance-lab

Notebook `data-governance-lab/data_governance_lab.ipynb` chứa **7 phần** tương tác, song song với project `medviet-governance/`:

| Phần | Nội dung | Trạng thái |
|:----:|----------|:---------:|
| 0 | Cài đặt môi trường (pip, spaCy, AGT) | 🚧 Cần chạy |
| 1 | Chuẩn bị dữ liệu (generate_patients) | ✅ Hoàn tất (qua medviet-governance) |
| 2 | PII Detection & Anonymization | ✅ Hoàn tất (src/pii/) |
| 3 | RBAC với Casbin | ✅ Hoàn tất (src/access/) |
| 4 | Mã hóa envelope | ✅ Hoàn tất (src/encryption/) |
| 5 | Kiểm tra chất lượng dữ liệu | ✅ Hoàn tất (src/quality/) |
| **6** | **Quản trị Agent với Microsoft AGT** | **⬜ Chưa chạy** |
| **7** | Ánh xạ tuân thủ NĐ13 | ✅ Hoàn tất (compliance_checklist.md) |

### Yêu cầu còn lại từ Notebook

**Phần 6 — Agent Governance với AGT:**
- Cài đặt `agent-governance-toolkit` (pip hoặc từ local source)
- Chạy cell thiết lập AGT PolicyEvaluator
- Chạy cell đánh giá agent actions (allow/deny)
- Chạy cell thực thi StatelessKernel
- **Bài 6.1:** Bổ sung rules vào `policies/medviet-data-policy.yaml`:
  - ✅ Cho phép agent `data_analyst` chỉ đọc dataset `aggregated`
  - ✅ Yêu cầu phê duyệt con người trước hành động `delete`

**Phần 7 — Compliance Mapping:**
- ✅ Đã hoàn tất qua `compliance_checklist.md` và `report.md`

---

## Danh Sách Công Việc Chi Tiết

### Phase 1: Tạo Work Plan & Report (10 phút)
- [x] Tạo `work_plan.md` — kế hoạch chi tiết
- [x] Tạo `report.md` — báo cáo tổng hợp

### Phase 2: Phần 1 — Chuẩn Bị Dữ Liệu (15 phút)
- [x] Chạy `scripts/generate_data.py` để tạo `data/raw/patients_raw.csv`
- [x] Kiểm tra dữ liệu đầu ra (200 records)
- [x] Liệt kê các cột PII (7 columns)

### Phase 3: Phần 2 — PII Detection & Anonymization (45 phút)
- [x] **`src/pii/detector.py`**: Hoàn thiện regex CCCD (11-12 digits), phone (optional 0 prefix), email, person
- [x] **`src/pii/anonymizer.py`**: Implement replace/mask/hash strategies, anonymize_dataframe
- [x] **`tests/test_pii.py`**: Hoàn thiện assert statements
- [x] Chạy pytest kiểm tra detection rate = **100%** (≥95% ✅)

### Phase 4: Phần 3 — RBAC với Casbin & FastAPI (45 phút)
- [x] **`src/access/policy.csv`**: Hoàn thiện policy rules (4 roles)
- [x] **`src/access/rbac.py`**: Điền status codes (401, 403), enforcer params
- [x] **`src/api/main.py`**: Implement 4 endpoints

### Phase 5: Phần 4 — Encryption (30 phút)
- [x] **`src/encryption/vault.py`**: Hoàn thiện encrypt_data, decrypt_data (AES-256-GCM)

### Phase 6: Phần 5 — Data Quality Validation (20 phút)
- [x] **`src/quality/validation.py`**: Điền column names, values, email regex
- [x] Implement `validate_anonymized_data`

### Phase 7: Phần 6 — Security Scanning (20 phút)
- [x] Tạo `.github/hooks/pre-commit` với git-secrets + Bandit + pip-audit
- [x] Tạo thư mục `reports/`
- [x] Chạy Bandit scan và lưu báo cáo (0 medium/high issues)

### Phase 8: Phần 7 — OPA Policy (15 phút)
- [x] **`policies/opa_policy.rego`**: Hoàn thiện data analyst & intern rules

### Phase 9: Phần 8 — Compliance Checklist (15 phút)
- [x] **`compliance_checklist.md`**: Điền DPO: Trần Mạnh Chánh Quân — quan.tm@medviet.ai
- [x] Mô tả technical solutions cho các mục còn thiếu

### Phase 10: Hoàn Tất & Kiểm Tra (15 phút)
- [x] Chạy toàn bộ test suite: **6/6 tests passed**
- [x] Kiểm tra tất cả file đã hoàn thiện
- [x] Cập nhật `compliance_checklist.md` sau khi hoàn tất
- [x] Git commit & push lên GitHub

---

## Ma Trận File Đã Hoàn Thiện

| File | Trạng thái | Ghi chú |
|------|-----------|---------|
| `work_plan.md` | ✅ Hoàn tất | Kế hoạch chi tiết |
| `report.md` | ✅ Hoàn tất | Báo cáo tổng hợp cuối cùng |
| `src/pii/detector.py` | ✅ Hoàn tất | Regex CCCD 11-12 digits, SĐT optional 0 prefix, email, person |
| `src/pii/anonymizer.py` | ✅ Hoàn tất | 3 strategies (replace/mask/hash), anonymize_dataframe |
| `tests/test_pii.py` | ✅ Hoàn tất | 6/6 tests PASSED — detection rate 100% |
| `src/access/policy.csv` | ✅ Hoàn tất | 4 roles RBAC (admin, ml_engineer, data_analyst, intern) |
| `src/access/rbac.py` | ✅ Hoàn tất | Casbin enforcer + FastAPI decorator (401/403) |
| `src/api/main.py` | ✅ Hoàn tất | 4 endpoints + health check |
| `src/encryption/vault.py` | ✅ Hoàn tất | AES-256-GCM envelope encryption round-trip |
| `src/quality/validation.py` | ✅ Hoàn tất | Great Expectations suite + validate function |
| `policies/opa_policy.rego` | ✅ Hoàn tất | ABAC rules đầy đủ |
| `.github/hooks/pre-commit` | ✅ Hoàn tất | git-secrets + Bandit + pip-audit |
| `compliance_checklist.md` | ✅ Hoàn tất | DPO + technical solutions NĐ13 |
| `reports/bandit_report.json` | ✅ Hoàn tất | 0 medium/high issues |

---

## Tiêu Chí Đánh Giá (100 điểm)

| Hạng mục | Điểm | Tiêu chí |
|---------|------|---------|
| PII Detection | 25đ | Detection rate ≥ 95%; CCCD + phone + email detect được |
| Anonymization | 20đ | PII gốc không còn trong output; non-PII columns giữ nguyên |
| RBAC API | 20đ | 4 roles hoạt động đúng; 403 đúng chỗ |
| Encryption | 15đ | Envelope encryption round-trip thành công |
| Security Audit | 10đ | git-secrets hook chặn credential; Bandit report |
| Compliance | 10đ | NĐ13 mapping đầy đủ, technical controls cụ thể |

**Ngưỡng đạt: ≥ 70/100 điểm**