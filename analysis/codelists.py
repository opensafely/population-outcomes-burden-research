from cohortextractor import codelist, codelist_from_csv
stroke = codelist_from_csv(
    "codelists/opensafely-incident-non-traumatic-stroke.csv",
    system="ctv3",
    column="CTV3ID",
)
stroke_hospital = codelist_from_csv(
    "codelists/opensafely-stroke-secondary-care.csv", system="icd10", column="icd"
)
aki_codes = codelist(
    ["N17", "N170", "N171", "N172", "N178", "N179"], system="icd10"
)
mi_codes = codelist_from_csv(
    "codelists/opensafely-myocardial-infarction-2.csv",
    system="ctv3",
    column="CTV3Code",
)
mi_codes_hospital = codelist_from_csv(
    "codelists/opensafely-cardiovascular-secondary-care.csv",
    system="icd10",
    column="icd",
    category_column="mi",
)
heart_failure_codes = codelist_from_csv(
    "codelists/opensafely-heart-failure.csv",
    system="ctv3",
    column="CTV3ID",
)
heart_failure_codes_hospital = codelist_from_csv(
    "codelists/opensafely-cardiovascular-secondary-care.csv",
    system="icd10",
    column="icd",
    category_column="heartfailure",
)
vte_codes_gp = codelist_from_csv(
    "codelists/opensafely-incident-venous-thromboembolic-disease.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="type",
)
vte_codes_hospital = codelist_from_csv(
    "codelists/opensafely-venous-thromboembolic-disease-hospital.csv",
    system="icd10",
    column="ICD_code",
    category_column="type",
)
covid_codelist = codelist_from_csv(
    "codelists/opensafely-covid-identification.csv",
    system="icd10",
    column="icd10_code",
)
ketoacidosis_codes = codelist_from_csv(
    "codelists/opensafely-diabetic-ketoacidosis-secondary-care.csv",
    system="icd10",
    column="icd10_code",
)
