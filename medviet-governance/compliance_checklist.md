# NĐ13/2023 Compliance Checklist — MedViet AI Platform

**Học viên:** Trần Mạnh Chánh Quân  
**Mã học viên:** 2A202600786  
**Ngày cập nhật:** 30/06/2026

---

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [ ] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [ ] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: Trần Mạnh Chánh Quân — email: quan.tm@medviet.ai

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) — phát hiện & ẩn danh CCCD, SĐT, email, họ tên | ✅ Done | AI Team |
| Access control | RBAC (Casbin) — 4 roles (admin, ml_engineer, data_analyst, intern) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption at rest | AES-256-GCM envelope encryption (SimpleVault) — KEK encrypts DEK, DEK encrypts data | 🚧 In Progress | Infra Team |
| Encryption in transit | FastAPI chạy HTTPS với TLS 1.3 (cần cấu hình thêm) | ⬜ Todo | Infra Team |
| Audit logging | API access logs qua middleware FastAPI + CloudTrail cho AWS deployment | 🚧 In Progress | Platform Team |
| Breach detection | Prometheus + Grafana monitoring (docker-compose.yml); Bandit SAST scan trong pre-commit hook | 🚧 In Progress | Security Team |

## F. Technical Solutions cho các mục còn thiếu

### F.1 Right to Erasure (Xóa dữ liệu theo yêu cầu)
- **Giải pháp:** Xây dựng endpoint API `/api/patients/{patient_id}/consent` cho phép user rút consent.
- **Cơ chế:** Khi user rút consent, dùng `delete_patient` endpoint (đã implement) để xóa toàn bộ dữ liệu của bệnh nhân đó khỏi raw dataset.
- **Audit:** Log timestamp của action rút consent vào file `audit/consent_revocation.log`.

### F.2 Breach Notification 72h
- **Giải pháp:** Xây dựng incident response pipeline:
  1. Prometheus alert manager phát hiện anomaly (số lượng request bất thường, pattern truy cập lạ)
  2. Alert gửi đến email/Slack của Security Team
  3. Script tự động gửi báo cáo đến cơ quan có thẩm quyền qua API (VD: Bộ Công an, Cục ATTT)
  4. Template báo cáo breach notification đã soạn sẵn trong `incidents/breach_report_template.md`

### F.3 Audit Logging
- **Giải pháp:** Implement middleware trong FastAPI để log mọi request:
  ```python
  @app.middleware("http")
  async def log_requests(request, call_next):
      response = await call_next(request)
      with open("audit/api_access.log", "a") as f:
          f.write(f"{datetime.utcnow()} | {request.method} {request.url.path} | {response.status_code}\n")
      return response
  ```
- **Lưu trữ:** Log được lưu trong 90 ngày, sau đó compressed archive.
- **Cloud:** Khi deploy lên AWS, dùng CloudTrail + S3 cho audit trail.

### F.4 Encryption in Transit
- **Giải pháp:** Cấu hình FastAPI với SSL/TLS certificate (Let's Encrypt hoặc internal CA).
- **Implementation:** Dùng Uvicorn với `--ssl-keyfile` và `--ssl-certfile`.
- **TLS version:** Chỉ cho phép TLS 1.3, tắt TLS 1.0/1.1 và SSLv3.

### F.5 Phát hiện xâm nhập (Breach Detection)
- **Giải pháp:** 
  - Prometheus metrics collection: `/metrics` endpoint export request count, latency, error rate
  - Grafana dashboard: Theo dõi real-time anomaly detection
  - Alert rules: P95 latency > 1s, error rate > 5%, số lượng 403 errors tăng đột biến
  - Bandit SAST scan tích hợp trong pre-commit hook (git-secrets + bandit + pip-audit)
  - TruffleHog scan định kỳ để phát hiện credential leak trong git history