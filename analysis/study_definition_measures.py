from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
)

csvt_codes = codelist(["G08X", "I636", "I676"], system="icd10")

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1980-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.05,
    },
    index_date="2019-02-01",
    population=patients.all(),
    CSVT_G08X=patients.admitted_to_hospital(
        with_these_diagnoses=codelist(["G08X"], system="icd10"),
        between=["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 0.05},
    ),
    CSVT_I636_I676=patients.admitted_to_hospital(
        with_these_diagnoses=codelist(["I636", "I676"], system="icd10"),
        between=["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 0.05},
    ),
)


measures = [
    Measure(
        id="CSVT_G08X_rate",
        numerator="CSVT_G08X",
        denominator="population",
        group_by="population",
    ),
    Measure(
        id="CSVT_I636_I676_rate",
        numerator="CSVT_I636_I676",
        denominator="population",
        group_by="population",
    ),
]
