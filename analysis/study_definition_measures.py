from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
)
from codelists import covid_codelist

csvt_codes = codelist(["G08X", "I636", "I676"], system="icd10")

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1980-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.05,
    },
    index_date="2019-02-01",
    population=patients.satisfying(
        """
            has_follow_up
        AND (age >=18 AND age <= 110)
        """,
        has_follow_up=patients.registered_with_one_practice_between(
            "index_date - 1 year", "index_date"
        ),
        age=patients.age_as_of(
            "index_date",
            return_expectations={
                "rate": "universal",
                "int": {"distribution": "population_ages"},
            },
        ),
    ),
    covid_hospitalisation=patients.categorised_as(
        {
            "COVID-19 positive": "covid_positive AND NOT covid_hospitalised",
            "COVID-19 hospitalised": "covid_hospitalised",
            "General population": "DEFAULT",
        },
        return_expectations={
            "incidence": 1,
            "category": {
                "ratios": {
                    "COVID-19 positive": 0.1,
                    "COVID-19 hospitalised": 0.1,
                    "General population": 0.8,
                }
            },
        },
        covid_positive=patients.with_test_result_in_sgss(
            pathogen="SARS-CoV-2",
            test_result="positive",
            between=["2020-01-01", "last_day_of_month(index_date)"],
            date_format="YYYY-MM-DD",
            return_expectations={"date": {"earliest": "index_date"}},
        ),
        covid_hospitalised=patients.admitted_to_hospital(
            with_these_diagnoses=covid_codelist,
            between=["2020-01-01", "last_day_of_month(index_date)"],
            return_expectations={"incidence": 0.20},
        ),
    ),
    CSVT=patients.satisfying(
        "CSVT_hospital OR CSVT_ons",
        CSVT_hospital=patients.admitted_to_hospital(
            with_these_diagnoses=csvt_codes,
            between=["index_date", "last_day_of_month(index_date)"],
            return_expectations={"incidence": 0.05},
        ),
        CSVT_ons=patients.with_these_codes_on_death_certificate(
            csvt_codes,
            between=["index_date", "last_day_of_month(index_date)"],
            return_expectations={"incidence": 0.05},
        ),
    ),
)


measures = [
    Measure(
        id="CSVT_rate",
        numerator="CSVT",
        denominator="population",
        group_by=["covid_hospitalisation"],
    ),
]
