import pandas as pd

# ✅ 0) 입력 CSV 파일명
INPUT_FILE = "seoul_library_202511.csv"

# ✅ 1) CSV 로드 (CSV만)
df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig", low_memory=False)

# ✅ 2) 기본 점검
print("shape:", df.shape)
print(df.head(3))
print(df.dtypes)

# ✅ 3) 불필요 컬럼 제거(예: Unnamed: 13)
drop_cols = [c for c in df.columns if str(c).startswith("Unnamed")]
df = df.drop(columns=drop_cols, errors="ignore")

# ✅ (필수) 대출건수 숫자 변환(집계하려면 필요)
if "대출건수" in df.columns:
    df["대출건수"] = pd.to_numeric(df["대출건수"], errors="coerce").fillna(0).astype(int)
else:
    raise KeyError("컬럼 '대출건수'가 없습니다. 파일 컬럼명을 확인해 주세요.")

# ✅ 3) 발행년도만 정리 (4자리만 뽑아서 숫자로)
if "발행년도" in df.columns:
    df["발행년도"] = (
        df["발행년도"]
        .astype("string")
        .str.extract(r"(\d{4})")[0]
    )
    df["발행년도"] = pd.to_numeric(df["발행년도"], errors="coerce").astype("Int64")
else:
    print("⚠️ 컬럼 '발행년도'가 없어서 발행년도 정리는 스킵합니다.")

# ✅ 4) 중복 제거: 도서명 + 저자 기준
if ("도서명" not in df.columns) or ("저자" not in df.columns):
    raise KeyError("중복 제거를 위해 '도서명'과 '저자' 컬럼이 필요합니다. 파일 컬럼명을 확인해 주세요.")

df["dedup_key"] = (
    df["도서명"].astype("string").fillna("").str.strip()
    + "|"
    + df["저자"].astype("string").fillna("").str.strip()
)

df_dedup = df.drop_duplicates(subset=["dedup_key"], keep="first").copy()

# ✅ 6) 주제대분류 생성(주제분류번호 첫 자리) + 집계 기준 반영
# 주제분류번호 -> 주제대분류(0~9) 만들기
if "주제분류번호" in df_dedup.columns:
    df_dedup["주제대분류"] = (
        df_dedup["주제분류번호"]
        .astype("string")
        .str.extract(r"(\d)")[0]
    )
elif "주제대분류" not in df_dedup.columns:
    raise KeyError("주제대분류 집계를 위해 '주제분류번호' 또는 '주제대분류' 컬럼이 필요합니다.")

# (선택) 대분류명 매핑
kdc_map = {
    "0": "총류", "1": "철학", "2": "종교", "3": "사회과학", "4": "자연과학",
    "5": "기술과학", "6": "예술", "7": "언어", "8": "문학", "9": "역사"
}
df_dedup["주제대분류명"] = df_dedup["주제대분류"].astype("string").map(kdc_map)

# ✅ 주제대분류 기준 집계(합계/평균/도서수)
by_subject = (
    df_dedup.groupby(["주제대분류", "주제대분류명"], as_index=False)
    .agg(
        대출건수합계=("대출건수", "sum"),
        평균대출건수=("대출건수", "mean"),
        도서수=("dedup_key", "count")
    )
    .sort_values("대출건수합계", ascending=False)
)

# ✅ (선택) Top10 대출 도서
top10_cols = [c for c in ["도서명", "저자", "출판사", "발행년도", "대출건수", "주제대분류", "주제대분류명"] if c in df_dedup.columns]
top10 = df_dedup.sort_values("대출건수", ascending=False).head(10)[top10_cols]

# ✅ 저장
df_dedup.to_csv("library_clean.csv", index=False, encoding="utf-8-sig")
by_subject.to_csv("library_by_subject_major.csv", index=False, encoding="utf-8-sig")
top10.to_csv("library_top10.csv", index=False, encoding="utf-8-sig")

print("정제 데이터: library_clean.csv")
print("주제대분류 집계: library_by_subject_major.csv")
print("상위 10개: library_top10.csv")

print("\n[주제대분류 상위 10]")
print(by_subject.head(10))

print("\n[Top10 대출 도서]")
print(top10)



