import csv
import hashlib

SAMPLEID_COL='sampleID'
NCBI_ACC_COL = 'NCBI_accession'

def md5row(row):
    tmp = [getattr(row,SAMPLEID_COL)] + sorted(getattr(row,NCBI_ACC_COL))
    tmp = hashlib.md5(" ".join(tmp).encode('UTF-8')).hexdigest()
    return tmp


class MetadataTSVFile(object):
    """container for metadata tsv file
    """

    def __init__(self,fh):
        self.fh = fh
        self.samples = {}
        self._read()

    def _read(self):
        self.fh.seek(0)
        import pandas as pd
        x = pd.read_csv(self.fh, sep="\t")
        try:
            x[NCBI_ACC_COL] = x[NCBI_ACC_COL].str.split(";")
        except AttributeError:
            x[NCBI_ACC_COL] = [[] for x in x[NCBI_ACC_COL]]
            pass
        md5 = []
        for row in x.itertuples():
            md5.append(md5row(row))
        x['md5'] = md5
        self.samples=x
