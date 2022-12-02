from tqdm import tqdm

import lucene
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import FSDirectory
import org.apache.lucene.document as document

lucene.initVM()

from java.io import File

import glob
import os
import pandas as pd
pd.io.parquet.get_engine('auto')

indexPath = File("./index").toPath()
indexDir = FSDirectory.open(indexPath)
writerConfig = IndexWriterConfig(EnglishAnalyzer())
writer = IndexWriter(indexDir, writerConfig)


def indexRow(title_id, alt_names):
    doc = document.Document()
    doc.add(document.Field("title_id", title_id, document.TextField.TYPE_STORED))
    doc.add(document.Field("alt_names", alt_names, document.TextField.TYPE_STORED))
    writer.addDocument(doc)


def dataToIndex(file_path):
    path = "./data/extracted_data"
    parquet_files = glob.glob(os.path.join(path, "*.parquet"))
    df = pd.concat((pd.read_parquet(f) for f in parquet_files))
    
    index = df.index
    number_of_rows = len(index)
    print("Pocet zaznamov: " + str(number_of_rows))
    
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        indexRow(row['title_id'], row['alt_names'])
    
    writer.close()

if __name__ == "__main__":
    dataToIndex("./data/extracted_data/part-00000")