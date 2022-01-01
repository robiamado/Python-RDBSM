import os, datetime
from pathlib import Path

class db():
    def __init__(self, name:str=''):
        try:
            os.makedirs('dbs')
        except FileExistsError:
            pass
        self.name = name
        self.update_error = False
        self.rows = []
        self.cols = []
        self.elems_matrix = []
        # search for an exisitng .pydb and imports eventual data structures.
        if not self.imports():
            self.log('Process','Creation','Database \'' + self.name
                 + '\' has been created')
    # represent a db in tabular form.
    def __repr__(self):
        return_str = self.name + ':\n'
        cols_repr = []
        rows_repr = []
        elems_matrix_repr = []
        divs_repr = []
        return_repr = ''
        if len(self.rows) > 0:
            max_len_row = self.rows[0]
        else:
            max_len_row = '0'
        for row in self.rows:
            rows_repr.append(row + ' '*len(row) + ' | ')
            if len(row) > len(max_len_row):
                max_len_row = row
            i = 0
            while i < len(rows_repr):
                if len(rows_repr[i]) < len(max_len_row) and self.rows[i] != '':
                    rows_repr[i] = rows_repr[i] + ' '*(len(max_len_row)-len(rows_repr[i]))
                if self.rows[i] == '':
                    rows_repr[i] = ' '*len(max_len_row)*2 + ' | '
                i +=  1
        cols_repr.append(' '*2*len(max_len_row) + ' | ')
        divs_repr.append('-'*2*len(max_len_row) + '-|-')
        for col in self.cols:
            cols_repr.append(col + ' '*len(col) + ' | ')
            divs_repr.append('-'*2*len(col) + '-|-')
        i = 0
        while i < len(self.elems_matrix):
            j = 0
            elems_matrix_repr.append([])
            while j < len(self.elems_matrix[i]):
                elems_matrix_repr[i].append(
                    self.elems_matrix[i][j] + ' '*len(self.elems_matrix[i][j])
                    )
                if len(elems_matrix_repr[i][j]) > len(cols_repr[j+1]):
                    cols_repr[j+1] = cols_repr[j+1] + ' '*(
                        len(elems_matrix_repr[i][j]) - len(cols_repr[j+1])
                        )
                    divs_repr[j+1] = divs_repr[j+1] + '-'*(
                        len(elems_matrix_repr[i][j]) - len(divs_repr[j+1])
                        )
                elif len(elems_matrix_repr[i][j]) < len(cols_repr[j+1]):
                    elems_matrix_repr[i][j] = elems_matrix_repr[i][j] + ' '*(
                        len(cols_repr[j+1]) - len(elems_matrix_repr[i][j])
                        )
                j += 1
            i += 1
        for col_repr in cols_repr:
            return_repr = return_repr + col_repr
        return_repr = return_repr + '\n'
        for div_repr in divs_repr:
            return_repr = return_repr + div_repr
        return_repr = return_repr + '\n'
        i = 0
        while i < len(rows_repr):
            return_repr = return_repr + rows_repr[i]
            j = 0
            while j < len(elems_matrix_repr[i]):
                return_repr = return_repr + elems_matrix_repr[i][j]
                j += 1
            return_repr = return_repr + '\n'
            return_repr = return_repr + '-'*(len(rows_repr[i])-2) + '|' + '\n'
            i += 1
        if self.rows == self.cols and self.cols == self.elems_matrix and self.elems_matrix == []:
            return 'Error trying to print an empty db.'
        else:
            return return_repr
    # track db activity in .log file.
    def log(self, id='Unknown', type='Unknown', desc=''):
        f = open('dbs/' + self.name + '.log', 'at')
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        f.write(now + ' : ' + id + ' | ' + type + ' | '
                + desc + '\n')
        f.close()
    # save db to external .pydb file.
    def save(self):
        f = open('dbs/' + self.name + '.pydb', 'wb')
        f.write(self.format())
        f.close()
        self.log('Process','Save', 'Data was formatted '
                 'and saved to ' + self.name + '.pydb file')
    # delete existing .pydb database file.
    def delete(self):
        while True:
            confirm = 'y'
            if confirm == 'y':
                    path = os.getcwd().replace('\\', '/') + '/dbs/' + self.name
                    try:
                        os.remove(path + '.pydb')
                    except:
                        print('Error trying to delete unexisting ' + self.name + '.db')
                    break       
            elif confirm == 'n':
                break
    # clear existing .log databse file.
    def delog(self):
        while True:
            confirm = input('Are you sure you want to clear ' +
                           self.name + ' log? (y/n)')
            if confirm == 'y':
                f = open('dbs/' + self.name + '.log', 'wt')
                f.write('')
                f.close()
                break
            elif confirm == 'n':
                break
    # read data from .pydb file.
    def read(self, struct_to_read):
        f = open('dbs/' + self.name + '.pydb', 'rt')
        pydb_string = f.read()
        pydb_data = pydb_string.split('$')
        return_str = ''
        return_data = []
        for struct in pydb_data:
            struct = struct.split('#')
            if struct[0] == struct_to_read:
                return_str = return_str + struct[0] + ': '
                if struct[0] == 'elems':
                    elems_rows = struct[1].split('&')
                    for elems_row in elems_rows:
                        return_data.append(elems_row.split('%'))
                    return_str = return_str + str(return_data)
                else:
                    return_str = return_str + str(struct[1].split('%'))
                self.log('Process','Read','Data file was unformatted and \'' +
                        struct_to_read + '\' was read from ' + self.name +
                        '.pydb file')
        if return_str == '':
            print('Unable to read ' + struct_to_read + ' from ' +
                      self.name + '.pydb file')
        else: return return_str
    # write data directly to .pydb file.
    def write(self, rows=[], cols=[], elems=[]):
        temp_rows = self.rows[:]
        temp_cols = self.cols[:]
        temp_elems_matrix = self.elems_matrix[:][:]
        if type(elems) is not list:
            elems = [elems]
        if type(rows) is not list:
            rows = [rows]
        if type(cols) is not list:
            cols = [cols]
        for each_row in rows:
            if type(each_row) is str:
                if each_row not in temp_rows:
                    temp_rows.append(each_row)
                    temp_elems_matrix.append([])
                    for each_col in temp_cols:
                        temp_elems_matrix[-1].append('')
                elif elems == []:
                        print('Warning: fail in trying to write a row with '
                                'an already existing name.')
            else:
                print('Warning: fail in trying to write a row with '
                        'an invalid name.')
        for each_col in cols:
            if type(each_col) is str:
                if each_col not in temp_cols:
                    temp_cols.append(each_col)
                    i = 0
                    while i < len(temp_rows):
                        temp_elems_matrix[i].append('')
                        i += 1
                elif elems == []:
                    print('Warning: fail in trying to write a row with '
                            'an already existing name.')
            else:
                print('Warning: fail in trying to write a coloumn with '
                        'an invalid name.')
        for each_elem in elems:
            if rows != [] and cols != []:
                i = 0
                while i < len(rows):
                    j = 0
                    while j < len(temp_rows):
                        if rows[i] == temp_rows[j]:
                            break
                        j += 1
                    k = 0
                    while k < len(cols):
                        l = 0
                        while l < len(temp_cols):
                            if cols[k] == temp_cols[l]:
                                break
                            l += 1
                        if len(elems) == 1:
                            temp_elems_matrix[j][l] = elems[0]
                        elif len(rows) == 1 and len(elems) == len(cols):
                            temp_elems_matrix[j][l] = elems[l]
                        elif len(cols) == 1 and len(elems) == len(rows):
                            temp_elems_matrix[j][l] = elems[j]
                        else:
                            print('Warning: fail in trying to write multiple '
                                'elements')
                        k += 1
                    i += 1
            elif rows != [] and cols == []:
                i = 0
                while i < len(rows):
                    j = 0
                    while j < len(temp_rows):
                        if rows[i] == temp_rows[j]:
                            break
                        j += 1
                    k = 0
                    while k < len(temp_cols):
                        if len(elems) == 1:
                            temp_elems_matrix[j][k] = elems[0]
                        elif len(elems) == len(temp_cols):
                            temp_elems_matrix[j][k] = elems[k]
                        else:
                            print('Warning: fail in trying to write '
                                'too few or too many row elements.')
                            return None
                        k += 1
                    i += 1
            elif rows == [] and cols != []:
                i = 0
                while i < len(cols):
                    j = 0
                    while j < len(temp_cols):
                        if cols[i] == temp_cols[j]:
                            break
                        j += 1
                    k = 0
                    while k < len(temp_rows):
                        if len(elems) == 1:
                            temp_elems_matrix[k][j] = elems[0]
                        elif len(elems) == len(temp_rows):
                            temp_elems_matrix[k][j] = elems[k]
                        else:
                            print('Warning: fail in trying to write '
                                'too few or too many coloumn elements.')
                            return None
                        k += 1
                    i += 1

            else:
                print('Warning: fail in trying to write an element.')
        # temporary db formatting
        pydb_string = 'db#' + self.name + '$rows#'
        for row in temp_rows:
            pydb_string = pydb_string + row + '%'
        pydb_string = pydb_string.removesuffix('%')
        pydb_string = pydb_string + '$cols#'
        for col in temp_cols:
            pydb_string = pydb_string + col + '%'
        pydb_string = pydb_string.removesuffix('%')
        pydb_string = pydb_string + '$elems#'
        for elems_row in temp_elems_matrix:
            for elem in elems_row:
                pydb_string = pydb_string + elem + '%'
            pydb_string = pydb_string.removesuffix('%')
            pydb_string = pydb_string + '&'
        pydb_string = pydb_string = pydb_string.removesuffix('&')
        f = open('dbs/' + self.name + '.pydb', 'wb')
        f.write(pydb_string.encode('utf-8'))
        f.close()
        self.log('Process','Write','rows=' + str(rows) +
                 ', coloumns=' + str(cols) + ', elems' + str(elems))
    # import data from exising .pydb file.
    def imports(self, extension = None):
        if extension == None:
            existing_db = Path('dbs/' + self.name + '.pydb')
            if existing_db.is_file():
                print(self.name + '.pydb already existing and will be '
                    'imported.')
                f = open(existing_db)
                self.unformat(f)
                f.close()
                self.log('Process','Import','Data file was unformatted and' +
                            ' imported from ' + self.name + '.pydb file')
            return True
        elif extension == 'csv':
            existing_db = Path('imports/' + self.name + '.csv')
            if existing_db.is_file():
                print(self.name + '.csv already existing and will be '
                      'imported.')
                f = open(existing_db)
                self.unformat(f, 'csv')
                f.close()
                self.log('Process','Import','Data file was unformatted and' +
                            ' imported from ' + self.name + '.csv file')
                return True
        return False
    # format data to utf-8 byte before saving or writing to .pydb file.
    # uses # to separate data structures as $structure_name#structure_data.
    # elements are devided by % while matrix rows are devided by &.
    # to review char encoding.
    def format(self):
        pydb_string = 'db#' + self.name + '$rows#'
        for row in self.rows:
            if row.count('%') == 0 and row.count('#') == 0 and row.count('$') == 0 and row.count('&') == 0:
                pydb_string = pydb_string + row + '%'
            else:
                print('Error cannot save data format with %,$,&,# symbols in rows.')
                exit(0)
        pydb_string = pydb_string.removesuffix('%')
        pydb_string = pydb_string + '$cols#'
        for col in self.cols:
            if col.count('%') == 0 and col.count('#') == 0 and col.count('$') == 0 and col.count('&') == 0:
                pydb_string = pydb_string + col + '%'
            else:
                print('Error cannot save data format with %,$,&,# symbols in cols.')
                exit(0)
        pydb_string = pydb_string.removesuffix('%')
        pydb_string = pydb_string + '$elems#'
        for elems_row in self.elems_matrix:
            for elem in elems_row:
                if elem.count('%') == 0 and elem.count('#') == 0 and elem.count('$') == 0 and elem.count('&') == 0:
                    pydb_string = pydb_string + elem + '%'
                else:
                    print('Error cannot save data format with %,$,&,# symbols in cols.')
                    exit(0)
            pydb_string = pydb_string.removesuffix('%')
            pydb_string = pydb_string + '&'
        pydb_string = pydb_string = pydb_string.removesuffix('&')
        return pydb_string.encode('utf-8')
    # unformat .pydb file data and saves it to current object instance.
    # uses # to separate data structures as $structure_name#structure_data.
    # elements are devided by % while matrix rows are devided by &.
    # to review char encoding.
    def unformat(self, f, extension = None):
        if extension == None:
            pydb_string = f.read()
            pydb_data = pydb_string.split('$')
            for struct in pydb_data:
                struct = struct.split('#')
                if struct[0] == 'db':
                    self.name = struct[1]
                elif struct[0] == 'rows':
                    self.rows = struct[1].split('%')
                elif struct[0] == 'cols':
                    self.cols = struct[1].split('%')
                elif struct[0] == 'elems':
                    elems_rows = struct[1].split('&')
                    for elems_row in elems_rows:
                        self.elems_matrix.append(elems_row.split('%'))
        elif extension == 'csv':
            csv_lines = f.readlines()
            delimiter = ''
            for csv_line in csv_lines:
                if csv_line.count(',') >= 1:
                    delimiter = ','
                    break
                elif csv_line.count(';') >= 1:
                    delimiter = ';'
                    break
                elif csv_line.count('|') >= 1:
                    delimiter = '|'
                    break
                elif csv_line.count('\t') >= 1:
                    delimiter = '\t'
                    break
                elif csv_line.count(' ') >= 1:
                    delimiter = ' '
                    break
                else:
                    print('Error on import, invalid .csv format.')
            csv_rows = []
            csv_cols = []
            csv_elems = []
            i = 0
            while i < len(csv_lines):
                if csv_lines[i].count(delimiter) >= 1:
                    if csv_cols == []:
                        csv_cols = csv_lines[i].split(delimiter)[:]
                    else:
                        csv_rows.append(csv_lines[i].split(delimiter)[0])
                        csv_elems.append(csv_lines[i].split(delimiter)[0:])
                i += 1
            i = 0
            while i < len(csv_cols):
                csv_cols[i] = csv_cols[i].strip(' ')
                csv_cols[i] = csv_cols[i].strip('\n')
                i += 1
            i = 0
            while i < len(csv_rows):
                csv_rows[i] = csv_rows[i].strip(' ')
                csv_rows[i] = csv_rows[i].strip('\n')
                i += 1
            i = 0
            while i < len(csv_elems):
                j = 0
                while j < len(csv_elems[i]):
                    csv_elems[i][j] = csv_elems[i][j].strip(' ')
                    csv_elems[i][j] = csv_elems[i][j].strip('\n')
                    j += 1
                i += 1
            self.add(cols=csv_cols, elems=csv_elems)
    # adds rows, cols and/or elements.
    def add(self, rows=[], cols=[], elems=[]):
        if type(elems) is not list:
            elems = [elems]
        if type(rows) is not list:
            rows = [rows]
        if type(cols) is not list:
            cols = [cols]
        for each_row in rows:
            if type(each_row) is str:
                if each_row not in self.rows:
                    self.rows.append(each_row)
                    self.elems_matrix.append([])
                    if elems != []:
                        for each_col in self.cols:
                            self.elems_matrix[-1].append('')
                else:
                    print('Warning: fail in trying to add a row with '
                         'an already existing name.')
            else:
                print('Warning: fail in trying to add a row with '
                        'an invalid name.')
        for each_col in cols:
            if type(each_col) is str:
                if each_col not in self.cols:
                    self.cols.append(each_col)
                    i = 0
                    while i < len(self.rows):
                        self.elems_matrix[i].append('')
                        i += 1
                    if elems != [] and self.elems_matrix != []:
                        if len(elems) <= len(self.elems_matrix[0]):
                            i = 0
                            while i < len(elems):
                                self.elems_matrix[0][i] = elems[i]
                                i += 1
                        elif len(elems) > len(self.elems_matrix[0]):
                            print('Warning: fail in trying to add a number of '
                            'elements exceeding the row length.')
            else:
                print('Warning: fail in trying to add a coloumn with '
                        'an invalid name.')
        for each_elem in elems:
            if rows != [] and cols != []:
                i = 0
                while i < len(rows):
                    j = 0
                    while j < len(self.rows):
                        if rows[i] == self.rows[j]:
                            break
                        j += 1
                    k = 0
                    while k < len(cols):
                        l = 0
                        while l < len(self.cols):
                            if cols[k] == self.cols[l]:
                                break
                            l += 1
                        if len(elems) == 1:
                            self.elems_matrix[j][l] = elems[0]
                        elif len(rows) == 1 and len(elems) == len(cols):
                            self.elems_matrix[j][l] = elems[l]
                        elif len(cols) == 1 and len(elems) == len(rows):
                            self.elems_matrix[j][l] = elems[j]
                        else:
                            print('Warning: fail in trying to add multiple '
                                'elements.')
                            return None
                        k += 1
                    i += 1
            elif rows != [] and cols == []:
                i = 0
                while i < len(rows):
                    j = 0
                    while j < len(self.rows):
                        if rows[i] == self.rows[j]:
                            break
                        j += 1
                    k = 0
                    while k < len(self.cols):
                        if len(elems) == 1:
                            self.elems_matrix[j][k] = elems[0]
                        elif len(elems) == len(self.cols):
                            self.elems_matrix[j][k] = elems[k]
                        else:
                            print('Warning: fail in trying to add '
                                'too few or too many row elements.')
                            return None
                        k += 1
                    i += 1
            elif rows == [] and cols != []:
                if len(each_elem) == len(cols):
                    self.rows.append('')
                    self.elems_matrix.append(each_elem)
                else:
                    i = 0
                    while i < len(cols):
                        j = 0
                        while j < len(self.cols):
                            if cols[i] == self.cols[j]:
                                break
                            j += 1
                        k = 0
                        while k < len(self.rows):
                            if len(elems) == 1:
                                self.elems_matrix[k][j] = elems[0]
                            elif len(elems) == len(self.rows):
                                self.elems_matrix[k][j] = elems[k]
                            else:
                                print('Warning: fail in trying to add '
                                    'too few or too many coloumn elements.')
                                return None
                            k += 1
                        i += 1
            else:
                print('Warning: fail in trying to add an element.')
        self.log('Process','Add','rows=' + str(rows) +
                 ', coloumns=' + str(cols) + ', elems' + str(elems))
    # returns an element row and coloumn or rows and coloumns of an element.
    def get(self, rows=[], cols=[], elems=[]):
        if type(elems) is not list:
            elems = [elems]
        if type(rows) is not list:
            rows = [rows]
        if type(cols) is not list:
            cols = [cols]
        return_value = []
        for each_row in rows:
            if type(each_row) is str:
                if each_row not in self.rows:
                    print('Warning: fail in trying to get a row with '
                                'unexisting name.')
                elif elems == [] and cols == []:
                    i = 0
                    while i < len(self.rows):
                        if each_row == self.rows[i]:
                            break
                        i += 1
                    j = 0
                    while j < len(self.cols):
                        return_value.append(self.elems_matrix[i][j])
                        j += 1
                    return return_value
            else:
                print('Warning: fail in trying to get a row with '
                        'an invalid name.')
        for each_col in cols:
            if type(each_col) is str:
                if each_col not in self.cols:
                    print('Warning: fail in trying to get a coloumn with '
                                'unexisting name.')
                elif elems == [] and rows == []:
                    i = 0
                    while i < len(self.cols):
                        if each_col == self.cols[i]:
                            break
                        i += 1
                    j = 0
                    while j < len(self.rows):
                        return_value.append(self.elems_matrix[i][j])
                        j += 1
                    return return_value
            else:
                print('Warning: fail in trying to get a row with '
                        'an invalid name.')
        for each_elem in elems:
            if rows == [] and cols == []:
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            rows.append(self.rows[i])
                            cols.append(self.cols[j])
                        j += 1
                    i += 1
            elif rows != [] and cols == []:
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            if self.rows[i] in rows:
                                cols.append(self.cols[j])
                        j += 1
                    i += 1
            elif cols != [] and rows == []:
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            if self.cols[j] in cols:
                                rows.append(self.rows[i])
                        j += 1
                    i += 1
            elif cols != [] and rows != []:
                rows_temp = rows[:]
                cols_temp = cols[:]
                rows = []
                cols = []
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            if self.rows[i] in rows_temp and (
                                self.cols[j] in cols_temp):
                                rows.append(self.rows[i])
                                cols.append(self.cols[j])
                        j += 1
                    i += 1
            if rows == [] or cols == []:
                print('Error: unable to get element row and coloumn.')
                return None
            return_value.append('rows = ')
            for row in rows:
                return_value[0] = return_value[0] + row + ', '
            return_value[0] = return_value[0].rstrip(', ')
            return_value.append('cols = ')
            for col in cols:
                return_value[1] = return_value[1] + col + ', '
            return_value[1] = return_value[1].rstrip(', ')
            return return_value
    # removes rows, cols and/or elements.
    def remove(self, rows=[], cols=[], elems=[]):
        if type(elems) is not list:
            elems = [elems]
        if type(rows) is not list:
            rows = [rows]
        if type(cols) is not list:
            cols = [cols]
        for each_row in rows:
            if type(each_row) is str:
                if each_row not in self.rows:
                    print('Warning: fail in trying to remove a row with '
                                'unexisting name.')
                elif elems == []:
                    self.rows.remove(each_row)
                    i = 0
                    while i < len(self.rows):
                        if each_row == self.rows[i]:
                            break
                        i += 1
                    self.elems_matrix.pop(i)
            else:
                print('Warning: fail in trying to remove a row with '
                        'an invalid name.')
        for each_col in cols:
            if type(each_col) is str:
                if each_col not in self.cols:
                    print('Warning: fail in trying to get a coloumn with '
                                'unexisting name.')
                elif elems == []:
                    i = 0
                    while i < len(self.cols):
                        if each_col == self.cols[i]:
                            break
                        i += 1
                    self.cols.remove(each_col)
                    j = 0
                    while j < len(self.rows):
                        self.elems_matrix[j].pop(i)
                        j += 1
            else:
                print('Warning: fail in trying to get a coloumn with '
                        'an invalid name.')
        for each_elem in elems:
            if rows == [] and cols == []:
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            self.elems_matrix[i][j] = ''
                        j += 1
                    i += 1
            elif rows != [] and cols == []:
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            if self.rows[i] in rows:
                                self.elems_matrix[i][j] = ''
                        j += 1
                    i += 1
            elif cols != [] and rows == []:
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            if self.cols[j] in cols:
                                self.elems_matrix[i][j] = ''
                        j += 1
                    i += 1
            elif cols != [] and rows != []:
                rows_temp = rows[:]
                cols_temp = cols[:]
                rows = []
                cols = []
                i = 0
                while i < len(self.elems_matrix):
                    j = 0
                    while j < len(self.elems_matrix[i]):
                        if each_elem == self.elems_matrix[i][j]:
                            if self.rows[i] in rows_temp and (
                                self.cols[j] in cols_temp):
                                self.elems_matrix[i][j] = ''
                        j += 1
                    i += 1
            self.log('Process','Remove','rows=' + str(rows) +
                 ', coloumns=' + str(cols) + ', elems' + str(elems))