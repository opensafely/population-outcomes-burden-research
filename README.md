# Changes in the rate of cardiometabolic and pulmonary events during the COVID-19 pandemic

This is the code and configuration for our paper, "Changes in the rate of cardiometabolic and pulmonary events during the COVID-19 pandemic".

* The paper has been submitted to medRxiv, and will appear [here](https://doi.org/10.1101/2021.02.17.21251812) soon.
* Raw model outputs, including charts, crosstabs, etc, are in [released_output](./released_output/)
* If you are interested in how we defined our variables, take a look at the study definitions in [analysis](./analysis/); this is written in `python`, but non-programmers should be able to understand what is going on there
* If you are interested in how we defined our code lists, look in the [codelists folder](./codelists/).

# About the OpenSAFELY framework

The OpenSAFELY framework is a secure analytics platform for
electronic health records research in the NHS.

Instead of requesting access for slices of patient data and
transporting them elsewhere for analysis, the framework supports
developing analytics against dummy data, and then running against the
real data *within the same infrastructure that the data is stored*.
Read more at [OpenSAFELY.org](https://opensafely.org).
