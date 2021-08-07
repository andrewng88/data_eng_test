# Data Engineer Assignment

### Step 1
```git clone https://github.com/andrewng88/data_eng_test.git```

```cd data_eng_test```

### Step 2 ( optional )
```pip install pandas```

### Step 3 ( To Run API extraction)
```python extract_api.py```

### Step 4 ( To Run UnitTest)
```python -m unittest test_covid.py```

**Directory structure:**
```
\.
│   extract_api.py <-- api extraction 
│   readme.md
│   secret_location.ini <-- config 
│   test_covid.py <-- unittest 
│   test_covid_compare.py <-- custom function for unittest
│
├───output
│       covid_api.log <-- output log
│       covid_data.xls <-- output xls
│
├───secret_location
│       secret_location.xlsx <-- excel file with information for API to pull
│
├───misc
│       Coding Challenge.docx
│       Data Engineer - Job Description.pdf
│       extract_api.ipynb
```