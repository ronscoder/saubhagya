import string

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Utility:
    def parse_cell(cell):
        col, row = 0,0
        for c in cell:
            if c in string.ascii_letters:
                col = col * 26 + (ord(c.upper()) - ord('A')) + 1
            else:
                row = c
        return int(row)-1, col-1
    
    def msg(label, value='', status = 'K'):
        statc = bcolors.OKBLUE
        if(status == 'H'):
            statc = bcolors.HEADER
        if(status == 'K'):
            statc = bcolors.OKGREEN
        if(status == 'E'):
            statc = bcolors.FAIL
            
        m = '{:30}\t{}'.format(label[:30], value) if not value=='' else '{}'.format(label)
        print(statc + m + bcolors.ENDC)
        return m
        
class Fields:
    pass
