import pandas as pd
from utility import Utility
from validations import Validations as val
import datetime


class Habitation:
    DISTRICT = 'B2' #22
    BLOCK = 'B3'
    DATA_ROW = 'A7'
    COLUMNS = ('SLNO','VILLAGE', 'CC', 'HAB', 'MAIN_HAB', 'STATUS','CATEGORY', 'HAB_TYPE', 
           'HH_TOT', 'HH_ELE_MET','HH_ELE_UNM', 'HH_BAL',
           'BPL_TOT', 'BPL_ELE_MET', 'BPL_ELE_UNM', 'BPL_BAL', 
           'MODE')
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_excel(filename,'HabitationDetail', header=None)
        self.reformat()
    
    def reformat(self):
        df = self.df
        # Check for format error
        # A6(5,0) shoould have Total, A7 should have 1
        if(not df.iloc[5,0] == 'Total'):
            err = 'File format error'
            info = 'Row 6 should be total column'
            Utility.msg(err, info, 'E')
            return False
        print(df.iloc[6])
        if(not int(df.iloc[6,0]) == 1):
            err = 'File format error'
            info = 'Row 7 should have the first record'
            Utility.msg(err, info, 'E')
            return False
        
        # District
        row, col = Utility.parse_cell(Habitation.DISTRICT)
        self.district = df.iloc[row, col]
        print('{:20}{}'.format('District', self.district))
        
        # Block
        row, col = Utility.parse_cell(Habitation.BLOCK)
        self.block = df.iloc[row, col]
        print('{:20}{}'.format('Block', self.block))
        
        # DATA
        row, col = Utility.parse_cell(Habitation.DATA_ROW)
        values = df.iloc[row:, :17].values
        self.df_habitat = pd.DataFrame(values, columns = Habitation.COLUMNS)
        self.df_habitat.fillna(0, inplace=True)
        print('data\n',self.df_habitat.head())
        return True
    
    def error(self,el,ok,msg):
        if(not ok):
            self.status.append(('E',el, msg))

    def verify(self):
        self.status = []            
        Utility.msg('Checking file...\n', self.filename, 'H')
        self.datarowidx, self.datacol = Utility.parse_cell(Habitation.DATA_ROW)
        for i, row in self.df_habitat.iterrows():                
            self.checkpoints(i,row)
        return {'filename': self.filename, 'date': str(datetime.datetime.now()), 'status': self.status}
    
    def checkpoints(self,i,row):            
        tabi = i+1
        el = 'SL.NO. {}(row:{}) {}'.format(row['SLNO'], tabi+self.datarowidx, row['HAB'])
        Utility.msg('Checking...', el, 'H')
        
        main_hab = row['MAIN_HAB']
        category = row['CATEGORY']
        status = row['STATUS']
        mode = row['MODE']
        hh = row['HH_TOT']
        hh_ele = row['HH_ELE_MET'] + row['HH_ELE_UNM']
        hh_bal = row['HH_BAL']
        bpl = row['BPL_TOT']
        bpl_ele = row['BPL_ELE_MET'] + row['BPL_ELE_UNM']
        bpl_bal = row['BPL_BAL']
        
        self.error(el,*val.check_select_value(main_hab, category, status, mode))
        self.error(el,*val.hh_equation(hh, hh_ele, hh_bal, bpl, bpl_ele, bpl_bal))
            
        # SL.NO. CHECK
        if(float(tabi) != float(row['SLNO'])):
            err = 'Sl.No not in good sequence'
            self.error(el, False, err)
            
        # Census Code
        """Every census code should have a main habitat (Y or Yes)
        """
        df = self.df_habitat
        main_hab_cen = df[df['CC'] == row['CC']]
        main_hab_cen = main_hab_cen[main_hab_cen['MAIN_HAB'] == 'Yes']
        if(main_hab_cen.empty):
            err = 'Main habitation not marked for census code {}'.format(row['CC'])
            self.error(el, False, err)
    
            
    def print_status(self):
        if(not len(self.status)):
            Utility.msg(self.filename, 'OK', 'K')
        else:
            print('*-*'*30)
            Utility.msg('File', self.filename)
            Utility.msg('{} errors found'.format(len(self.status)), status='H')
            
            for st in self.status:
                Utility.msg(st[1], st[2],status = 'E')
#            do_print = input('Save to file? y/n: ')
#            if(do_print == 'y'):
#                df = pd.DataFrame(self.status, columns=['el', 'msg'])
#                df = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
#                df.to_excel(self.filename + '_validation.xlsx')
