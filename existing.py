import pandas as pd
import math
import string
from utility import Utility

class GridExisting:
    SHEET_NO = 0
    DISTRICT = 'B1' #22
    BLOCK = 'B2'
    DATA_ROW = 'A5'
    COLUMNS = ('SLNO','VILLAGE', 'CENSUS CODE', 'HAB NAME', 'HAB CODE','11KV', 
               'LT 1P','LT 3P', 'LT 1P AB', 'LT 3P AB', 'DTR COUNT','KVA', 
               'KW DOM', 'KW AGRI', 'KW IND', 'KW PUB', 'KW OTH', 'KW TOTAL')
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_excel(filename, GridExisting.SHEET_NO , header=None)
    
    def reformat(self):
        df = self.df
        # District
        row, col = Utility.parse_cell(GridExisting.DISTRICT)
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
        row, col = Utility.parse_cell(GridExisting.BLOCK)
        if(not df.iloc[row,col-1] == 'Block'):
            err = 'File format error'
            info = 'Cell B1 should have Block label'
            Utility.msg(err, info, 'E')
            return False
        self.block = df.iloc[row, col]
        print('{:20}{}'.format('Block', self.block))
        
        # DATA
        row, col = Utility.parse_cell(GridExisting.DATA_ROW)
        values = df.iloc[row:].values
        self.df_existing = pd.DataFrame(values, columns = GridExisting.COLUMNS)
        self.df_existing.fillna(0, inplace=True)
        return True

    def verify(self):
        pass
    

    