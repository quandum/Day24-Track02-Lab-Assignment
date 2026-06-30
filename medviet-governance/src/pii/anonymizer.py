# src/pii/anonymizer.py
import hashlib
import random
import pandas as pd
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from faker import Faker
from .detector import build_vietnamese_analyzer, detect_pii

fake = Faker("vi_VN")

class MedVietAnonymizer:

    def __init__(self):
        self.analyzer = build_vietnamese_analyzer()
        self.anonymizer = AnonymizerEngine()

    def anonymize_text(self, text: str, strategy: str = "replace") -> str:
        """
        TODO: Anonymize text với strategy được chọn.

        Strategies:
        - "mask"    : Nguyen Van A → N****** V** A
        - "replace" : thay bằng fake data (dùng Faker)
        - "hash"    : SHA-256 one-way hash
        - "generalize": chỉ dùng cho tuổi/năm sinh
        """
        results = detect_pii(text, self.analyzer)
        if not results:
            return text

        # TODO: implement operators dict dựa trên strategy
        operators = {}

        if strategy == "replace":
            operators = {
                "PERSON": OperatorConfig("replace", 
                          {"new_value": fake.name()}),
                "EMAIL_ADDRESS": OperatorConfig("replace", 
                                 {"new_value": fake.email()}),   # TODO: fake email
                "VN_CCCD": OperatorConfig("replace", 
                           {"new_value": "".join(random.choices("0123456789", k=12))}),          # TODO: fake CCCD
                "VN_PHONE": OperatorConfig("replace", 
                            {"new_value": f"0{random.choice([3,5,7,8,9])}" + "".join(random.choices("0123456789", k=8))}),         # TODO: fake phone
            }
        elif strategy == "mask":
            operators = {
                "PERSON": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 50, "from_end": False}),
                "EMAIL_ADDRESS": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 50, "from_end": False}),
                "VN_CCCD": OperatorConfig("replace", {"new_value": "************"}),
                "VN_PHONE": OperatorConfig("replace", {"new_value": "0*********"}),
            }
        elif strategy == "hash":
            operators = {
                "PERSON": OperatorConfig("hash"),
                "EMAIL_ADDRESS": OperatorConfig("hash"),
                "VN_CCCD": OperatorConfig("hash"),
                "VN_PHONE": OperatorConfig("hash"),
            }

        anonymized = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators
        )
        return anonymized.text

    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        TODO: Anonymize toàn bộ DataFrame.
        - Cột text (ho_ten, dia_chi, email): dùng anonymize_text()
        - Cột cccd, so_dien_thoai: replace trực tiếp bằng fake data
        - Cột benh, ket_qua_xet_nghiem: GIỮ NGUYÊN (cần cho model training)
        - Cột patient_id: GIỮ NGUYÊN (pseudonym đã đủ an toàn)
        """
        df_anon = df.copy()

        # Cột text: dùng anonymize_text với strategy replace
        for col in ["ho_ten", "dia_chi", "email"]:
            df_anon[col] = df_anon[col].apply(
                lambda x: self.anonymize_text(str(x), strategy="replace")
            )

        # Cột cccd: replace trực tiếp bằng fake CCCD
        df_anon["cccd"] = df_anon["cccd"].apply(
            lambda x: "".join(random.choices("0123456789", k=12))
        )

        # Cột so_dien_thoai: replace trực tiếp bằng fake phone
        df_anon["so_dien_thoai"] = df_anon["so_dien_thoai"].apply(
            lambda x: f"0{random.choice([3,5,7,8,9])}" + "".join(random.choices("0123456789", k=8))
        )

        # Cột ngay_sinh: generalize thành năm sinh
        df_anon["ngay_sinh"] = df_anon["ngay_sinh"].apply(
            lambda x: str(x).split("/")[-1] if "/" in str(x) else str(x)
        )

        # Cột bac_si_phu_trach: anonymize
        df_anon["bac_si_phu_trach"] = df_anon["bac_si_phu_trach"].apply(
            lambda x: self.anonymize_text(str(x), strategy="replace")
        )

        # Cột ngay_kham: generalize thành tháng/năm
        df_anon["ngay_kham"] = df_anon["ngay_kham"].apply(
            lambda x: "/".join(str(x).split("/")[1:]) if "/" in str(x) else str(x)
        )

        # GIỮ NGUYÊN: benh, ket_qua_xet_nghiem, patient_id

        return df_anon

    def calculate_detection_rate(self, 
                                  original_df: pd.DataFrame,
                                  pii_columns: list) -> float:
        """
        TODO: Tính % PII được detect thành công.
        Mục tiêu: > 95%

        Logic: với mỗi ô trong pii_columns,
               kiểm tra xem detect_pii() có tìm thấy ít nhất 1 entity không.
        """
        total = 0
        detected = 0

        for col in pii_columns:
            for value in original_df[col].astype(str):
                total += 1
                results = detect_pii(value, self.analyzer)
                if len(results) > 0:
                    detected += 1

        return detected / total if total > 0 else 0.0