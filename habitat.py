import pandas as pd
import math
import string
from utility import Utility


class Habitat:
    DISTRICT = 'B2' #22
    BLOCK = 'B3'
    DATA_ROW = 'A7'
    COLUMNS = ('SLNO','VILLAGE', 'CENSUS CODE', 'HAB NAME', 'MAIN HAB', 'STATUS','CATEGORY', 'HAB TYPE', 
                   'HH TOTAL', 'HH ELECTRIFIED METERED','HH ELECTRIFIED UNMETERED', 'HH PROPOSED',
                   'BPL TOTAL', 'BPL ELECTRIFIED METERED', 'BPL ELECTRIFIED UNMETERED', 'BPL PROPOSED', 
                   'MODE ELECTRIFICATION')
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_excel(filename,'HabitationDetail', header=None)
    
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
        row, col = Utility.parse_cell(Habitat.DISTRICT)
        self.district = df.iloc[row, col]
        print('{:20}{}'.format('District', self.district))
        
        # Block
        row, col = Utility.parse_cell(Habitat.BLOCK)
        self.block = df.iloc[row, col]
        print('{:20}{}'.format('Block', self.block))
        
        # DATA
        row, col = Utility.parse_cell(Habitat.DATA_ROW)
        values = df.iloc[row:, :17].values
        self.df_habitat = pd.DataFrame(values, columns = Habitat.COLUMNS)
        self.df_habitat.fillna(0, inplace=True)
        print('data\n',self.df_habitat.head())
        return True
    
    
    def verify(self):
        self.status = []
        if(self.df_habitat is None):
            Utility.msg(self.filename, 'Data not formatted.', 'E')
            exit()
            
        Utility.msg('Checking file', self.filename, 'H')
        df = self.df_habitat
        datarowidx, datacol = Utility.parse_cell(Habitat.DATA_ROW)
        for i, row in df.iterrows():
            tabi = i+1

            el = 'SL.NO. {}(row:{}) {}'.format(row['SLNO'], tabi+datarowidx, row['HAB NAME'])
            Utility.msg('Checking...', el, 'H')
            
            # SL.NO. CHECK
            if(float(tabi) != float(row['SLNO'])):
                self.status.append(Utility.msg(el, 'SLNO. not proper', 'E'))
                
            # Census Code
            """Every census code should have a main habitat (Y or Yes)
            """
            yes = ('yes', 'Yes', 'YES', 'Y', 'y')
            main_hab = df[df['CENSUS CODE'] == row['CENSUS CODE']]
            main_hab = main_hab[main_hab['MAIN HAB'].isin(yes)]
            if(main_hab.empty):
                err = 'Main habitation not marked for census code {}'.format(row['CENSUS CODE'])
                self.status.append(Utility.msg(el, err, 'E'))
                
            # Electrified status should have non-zero electried HH
            st = ('EG', 'Electrified through grid')
            hh_elec = float(row['HH ELECTRIFIED METERED']) + float(row['HH ELECTRIFIED UNMETERED'])
            if(
                (not hh_elec > 0) 
                and 
                (row['STATUS'] in st)
            ):
                # print(row)
                err = 'Habitation electrified through grid should have electrified HH'
                self.status.append(Utility.msg(el, err, 'E'))
                
            # Category
            # cat = row['CATEGORY'].strip()
            """
            I:   No additional Infra required
                - No infra should be proposed
            II:  Significant Infra required
            III: Mixed of I & II
            """

            # Sum check
            if(hh_elec > row['HH TOTAL']):
                err = 'Electrified HH cant exceed total'
                self.status.append(Utility.msg(el, err, 'E'))
            bpel = float(row['BPL ELECTRIFIED METERED']) + float(row['BPL ELECTRIFIED UNMETERED'])
            if(bpel > row['BPL TOTAL']):
                err = 'Electrified BPL cant exceed total'
                self.status.append(Utility.msg(el, err, 'E'))
            if((row['HH PROPOSED'] == 0) and  row['HH TOTAL'] > hh_elec):
                err = 'HH left out!!'
                self.status.append(Utility.msg(el, err, 'E'))
            if((row['BPL PROPOSED'] == 0) and  row['BPL TOTAL'] > bpel):
                err = 'BPL left out!!'
                self.status.append(Utility.msg(el, err, 'E'))
            if(row['BPL PROPOSED'] > row['HH PROPOSED']):
                err = 'Extra BPL! Immigrants are not allowed'
                self.status.append(Utility.msg(el, err, 'E'))
            # Mode of elctrification
            # if mode of electrification is given, proposed should not be blank
            if(
                (row['MODE ELECTRIFICATION'] in ('Grid', 'Off-Grid')) 
                and 
                (
                    float((row['HH PROPOSED']+row['BPL PROPOSED']))== 0
                )):
                err = 'Proposed HH not given'
                self.status.append(Utility.msg(el, err, 'E'))

        self.print_status()
        return True
            
    def print_status(self):
        if(not len(self.status)):
            Utility.msg(self.filename, 'OK', 'K')
        else:
            print('*-*'*30)
            Utility.msg(self.filename, '\nErrors found ({})'.format(len(self.status)), 'E')
            for st in self.status:
                Utility.msg(st,status = 'E')
            do_print = input('Save to file? y/n: ')
            if(do_print == 'y'):
                df = pd.DataFrame(self.status, columns=['Msg'])
                df = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
                df.to_excel(self.filename + '_validation.xlsx')
