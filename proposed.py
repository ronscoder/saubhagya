import pandas as pd
import math
import string
from utility import Utility


class GridProposed:
    SHEET_NO = 2
    DISTRICT = 'B1' #22
    BLOCK = 'B2'
    DATA_ROW = 'A5'
    COLUMNS = ('SLNO','VILLAGE', 'CENSUS CODE', 'HAB NAME', 'HAB CODE',
               'BPL', 'NON BPL FREE', 'NON BPL NOT FREE','HH TOTAL', 
               'ACSR SQ TYPE', 'ACSR SQ LEN', 'ACSR WS TYPE', 'ACSR WS LEN', 'ACSR RB TYPE', 'ACSR RB LEN',
               'LT AB TYPE 1', 'LT AB LEN 1', 'LT AB TYPE 2','LT AB LEN 2', 
               'KVA 1', 'DTR COUNT 1', 'KVA 2', 'DTR COUNT 2'  )
    def __init__(self, filename):
        self.filename = filename
        df = pd.read_excel(filename, GridProposed.SHEET_NO , header=None)
        self.df = df
    
    def reformat(self):
        df = self.df
        # District
        row, col = Utility.parse_cell(GridProposed.DISTRICT)
        # Check for format error
        # A1 shoould have 'District', B2 should have 'Block'
        if(not df.iloc[row,col-1] == 'District'):
            err = 'File format error'
            info = 'Cell B1 should have District label'
            Utility.msg(err, info, 'E')
            return False        
        self.district = df.iloc[row, col]
        print('{:20}{}'.format('District', self.district))
        
        # Block
        row, col = Utility.parse_cell(GridProposed.BLOCK)
        if(not df.iloc[row,col-1] == 'Block'):
            err = 'File format error'
            info = 'Cell B1 should have Block label'
            Utility.msg(err, info, 'E')
            return False
        self.block = df.iloc[row, col]
        print('{:20}{}'.format('Block', self.block))
        
        # DATA
        row, col = Utility.parse_cell(GridProposed.DATA_ROW)
        values = df.iloc[row:].values
        self.df_proposed = pd.DataFrame(values, columns = GridProposed.COLUMNS)
        self.df_proposed.fillna(0, inplace=True)
        print('data\n',self.df_proposed.head())
        return True

    def print_status(self):
        if(not len(self.status)):
            Utility.msg(self.filename, 'OK', 'K')
        else:
            Utility.msg(self.filename, 'Errors found ({})'.format(len(self.status)), 'E')
            for st in self.status:
                print(st)

    def verify(self):
        self.status = []
        if(self.df_proposed is None):
            Utility.msg(self.filename, 'Data not formatted.', 'E')
            exit()
            
        Utility.msg('Checking file', self.filename, 'H')
        df = self.df_proposed
        datarowidx, datacol = Utility.parse_cell(GridProposed.DATA_ROW)
        for i, row in df.iterrows():
            tabi = i+1
            el = 'SL.NO. {}(row:{}) {}'.format(row['SLNO'], tabi+datarowidx, row['HAB NAME'])
            Utility.msg('Checking...', el, 'H')
            # SL.NO. CHECK
            if(float(tabi) != float(row['SLNO'])):
                self.status.append(Utility.msg(el, 'SLNO. not proper', 'E'))
            # 
        self.print_status()
        return True
            
