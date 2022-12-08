# VINF

## Štruktúra projektu:
VINF\
> NEW
- - - -
>> data (in .gitignore)
- - - -
>>> extracted_data
- - - -
>>>> _SUCCESS\
>>>> part-00000-d680c7b2-3b01-4cbb-ac4f-6546c62d0632-c000.snappy.parquet\
>>>> part-00001-d680c7b2-3b01-4cbb-ac4f-6546c62d0632-c000.snappy.parquet\
>>>> part-00002-d680c7b2-3b01-4cbb-ac4f-6546c62d0632-c000.snappy.parquet\
>>>> part-00003-d680c7b2-3b01-4cbb-ac4f-6546c62d0632-c000.snappy.parquet\
>>>> part-00004-d680c7b2-3b01-4cbb-ac4f-6546c62d0632-c000.snappy.parquet\
- - - -
>>> index (PyLucene index dir)\
- - - -
>>>> ...\
- - - -
>>> wikidata5m_entity\
- - - -
>> extractData\
- - - -
>>> extractData.py\
>>> requirements.txt\
- - - -
>> luceneIndexer\
- - - -
>>> luceneIndexer.py\
>>> requirements.txt\
- - - -
>> searching\
- - - -
>>> searching.py\
>>> requirements.txt\
- - - -
> OLD\
- - - -
>> data (in .gitignore)\
- - - -
>>> original_data_file.json\
>>> unique_data_file.json\
>>> wikidata5m_entity.txt\
- - - -
>> main.py\
>> process_data.py\
>> searching.py\
>> utils.py\
>> requirements.txt\
- - - -

## Spustenie kódu:

**OLD**\
cmd:
```
pip install -r requirements.txt
python main.py
```

**NEW**
* extractData.py
  Docker: https://hub.docker.com/r/iisas/hadoop-spark-pig-hive
  Treba do docker containeru presunúť ./extractData a ./data/wikidata5m_entity.txt.
  cmd:
  ```
  hadoop fs -copyFromLocal /extractData/data/wikidata5m_entity.txt. ./
  pip install -r /extractData/requirements.txt
  spark-submit /extractData/extractData.py
  hadoop fs -get ./extracted_data ./extractData
  ```
* luceneIndexer.py
  Docker: https://hub.docker.com/r/coady/pylucene\
  Treba do docker containeru presunúť ./luceneIndexer a ./extracted_data (získané z extractData.py)
  cmd:
  ```
  pip install -r /luceneIndexer/requirements.txt
  python /luceneIndexer/luceneIndexer.py
  ```
* searching.py
  Docker: https://hub.docker.com/r/coady/pylucene
  Treba do docker containeru presunúť ./searching a ./index (môže sa použiť rovnaký kontajner ako pri luceneIndexer.py tým pádom sa tam ./index bude nachádať)
  cmd:
  ```
  pip install -r /searching/requirements.txt
  python /searching/searching.py
  ```
