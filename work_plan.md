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

## Danh Sách Công Việc Chi Tiết

### Phase 1: Tạo Work Plan & Report (10 phút)
- [ ] Tạo `work_plan.md` — kế hoạch chi tiết
- [ ] Tạo `report.md` — báo cáo tổng hợp

### Phase 2: Phần 1 — Chuẩn Bị Dữ Liệu (15 phút)
- [ ] Chạy `scripts/generate_data.py` để tạo `data/raw/patients_raw.csv`
- [ ] Kiểm tra dữ liệu đầu ra
- [ ] Liệt kê các cột PII

### Phase 3: Phần 2 — PII Detection & Anonymization (45 phút)
- [ ] **`src/pii/detector.py`**: Hoàn thiện regex CCCD, regex phone, NLP model name, thêm recognizers
- [ ] **`src/pii/anonymizer.py`**: Implement replace/mask/hash strategies, anonymize_dataframe
- [ ] **`tests/test_pii.py`**: Hoàn thiện assert statements
- [ ] Chạy pytest kiểm tra detection rate ≥ 95%

### Phase 4: Phần 3 — RBAC với Casbin & FastAPI (45 phút)
- [ ] **`src/access/policy.csv`**: Hoàn thiện policy rules
- [ ] **`src/access/rbac.py`**: Điền status codes, enforcer params
- [ ] **`src/api/main.py`**: Implement 4 endpoints

### Phase 5: Phần 4 — Encryption (30 phút)
- [ ] **`src/encryption/vault.py`**: Hoàn thiện encrypt_data, decrypt_data

### Phase 6: Phần 5 — Data Quality Validation (20 phút)
- [ ] **`src/quality/validation.py`**: Điền column names, values, email regex
- [ ] Implement `validate_anonymized_data`

### Phase 7: Phần 6 — Security Scanning (20 phút)
- [ ] Tạo `.github/hooks/pre-commit` với git-secrets + Bandit + pip-audit
- [ ] Tạo thư mục `reports/`
- [ ] Chạy Bandit scan và lưu báo cáo

### Phase 8: Phần 7 — OPA Policy (15 phút)
- [ ] **`policies/opa_policy.rego`**: Hoàn thiện data analyst & intern rules

### Phase 9: Phần 8 — Compliance Checklist (15 phút)
- [ ] **`compliance_checklist.md`**: Điền đầy đủ thông tin DPO
- [ ] Mô tả technical solutions cho các mục còn thiếu

### Phase 10: Hoàn Tất & Kiểm Tra (15 phút)
- [ ] Chạy toàn bộ test suite: `pytest medviet-governance/tests/ -v --tb=short`
- [ ] Kiểm tra tất cả file đã hoàn thiện
- [ ] Cập nhật `compliance_checklist.md` sau khi hoàn tất

---

## Ma Trận File Cần Sửa

| File | Trạng thái | Ghi chú |
|------|-----------|---------|
| `work_plan.md` | ✅ Tạo mới | File này |
| `report.md` | ⬜ Tạo mới | Báo cáo tổng hợp cuối cùng |
| `src/pii/detector.py` | ⬜ Hoàn thiện | 5 TODO items |
| `src/pii/anonymizer.py` | ⬜ Hoàn thiện | 6 TODO items |
| `tests/test_pii.py` | ⬜ Hoàn thiện | 5 TODO items |
| `src/access/policy.csv` | ⬜ Hoàn thiện | 4 TODO comments |
| `src/access/rbac.py` | ⬜ Hoàn thiện | 4 TODO items |
| `src/api/main.py` | ⬜ Hoàn thiện | 4 empty endpoints |
| `src/encryption/vault.py` | ⬜ Hoàn thiện | 4 TODO items |
| `src/quality/validation.py` | ⬜ Hoàn thiện | 6 TODO items |
| `policies/opa_policy.rego` | ⬜ Hoàn thiện | 3 TODO blocks |
| `.github/hooks/pre-commit` | ⬜ Tạo mới | Security hook |
| `compliance_checklist.md` | ⬜ Cập nhật | Thêm DPO & technical solutions |

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