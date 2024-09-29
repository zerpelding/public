"""
HW-2 Data Table implementation.

NAME: Zoe Erpelding
DATE: Fall 2023
CLASS: CPSC 322

"""

import csv
import tabulate


class DataRow:
    """A basic representation of a relational table row. The row maintains
    its corresponding column information.

    """
    
    def __init__(self, columns=[], values=[]):
        """Create a row from a list of column names and data values.
           
        Args:
            columns: A list of column names for the row
            values: A list of the corresponding column values.

        Notes: 
            The column names cannot contain duplicates.
            There must be one value for each column.

        """
        if len(columns) != len(set(columns)):
            raise ValueError('duplicate column names')
        if len(columns) != len(values):
            raise ValueError('mismatched number of columns and values')
        self.__columns = columns.copy()
        self.__values = values.copy()

        
    def __repr__(self):
        """Returns a string representation of the data row (formatted as a
        table with one row).

        Notes: 
            Uses the tabulate library to pretty-print the row.

        """
        return tabulate.tabulate([self.values()], headers=self.columns())

        
    def __getitem__(self, column):
        """Returns the value of the given column name.
        
        Args:
            column: The name of the column.

        """
        if column not in self.columns():
            raise IndexError('bad column name')
        return self.values()[self.columns().index(column)]


    def __setitem__(self, column, value):
        """Modify the value for a given row column.
        
        Args: 
            column: The column name.
            value: The new value.

        """
        if column not in self.columns():
            raise IndexError('bad column name')
        self.__values[self.columns().index(column)] = value


    def __delitem__(self, column):
        """Removes the given column and corresponding value from the row.

        Args:
            column: The column name.

        """
        if column not in self.columns():
            raise IndexError('bad column name')
        del self.__values[self.columns().index(column)]
        del self.__columns[self.columns().index(column)] 

    
    def __eq__(self, other):
        """Returns true if this data row and other data row are equal.

        Args:
            other: The other row to compare this row to.

        Notes:
            Checks that the rows have the same columns and values.

        """
        if len(self.__columns) != len(other.columns()) or len(self.__values) != len(other.values()):
            return False
        for i in range(len(self.__columns)):
            if self.__columns[i] != other.columns()[i]:
                return False
            if self.__values[i] != other.values()[i]:
                return False
        return True

    
    def __add__(self, other):
        """Combines the current row with another row into a new row.
        
        Args:
            other: The other row being combined with this one.

        Notes:
            The current and other row cannot share column names.

        """
        if not isinstance(other, DataRow):
            raise ValueError('expecting DataRow object')
        if len(set(self.columns()).intersection(other.columns())) != 0:
            raise ValueError('overlapping column names')
        return DataRow(self.columns() + other.columns(),
                       self.values() + other.values())


    def columns(self):
        """Returns a list of the columns of the row."""
        return self.__columns.copy()


    def values(self, columns=None):
        """Returns a list of the values for the selected columns in the order
        of the column names given.
           
        Args:
            columns: The column values of the row to return. 

        Notes:
            If no columns given, all column values returned.

        """
        if columns is None:
            return self.__values.copy()
        if not set(columns) <= set(self.columns()):
            raise ValueError('duplicate column names')
        return [self[column] for column in columns]


    def select(self, columns=None):
        """Returns a new data row for the selected columns in the order of the
        column names given.

        Args:
            columns: The column values of the row to include.
        
        Notes:
            If no columns given, all column values included.

        """
        
        if columns == None:
            return DataRow(self.__columns.copy(), self.__values.copy())
        if not set(columns) <= set(self.columns()):
            raise ValueError('duplicate column names')
        if len(columns) != len(set(columns)):
            raise ValueError('duplicate column names')
        values = self.values(columns)
        return DataRow(columns, values)
        
    
    def copy(self):
        """Returns a copy of the data row."""
        return self.select()

    

class DataTable:
    """A relational table consisting of rows and columns of data.

    Note that data values loaded from a CSV file are automatically
    converted to numeric values.

    """
    
    def __init__(self, columns=[]):
        """Create a new data table with the given column names

        Args:
            columns: A list of column names. 

        Notes:
            Requires unique set of column names. 

        """
        if len(columns) != len(set(columns)):
            raise ValueError('duplicate column names')
        self.__columns = columns.copy()
        self.__row_data = []


    def __repr__(self):
        """Return a string representation of the table.
        
        Notes:
            Uses tabulate to pretty print the table.

        """
        all_data = [self.__columns]
        for row in self.__row_data:
            all_data.append(row.values())
        return tabulate.tabulate(all_data, headers="firstrow")
        

    
    def __getitem__(self, row_index):
        """Returns the row at row_index of the data table.
        
        Notes:
            Makes data tables iterable over their rows.

        """
        return self.__row_data[row_index]

    
    def __delitem__(self, row_index):
        """Deletes the row at row_index of the data table.

        """
        del self.__row_data[row_index]

        
    def load(self, filename, delimiter=','):
        """Add rows from given filename with the given column delimiter.

        Args:
            filename: The name of the file to load data from
            delimeter: The column delimiter to use

        Notes:
            Assumes that the header is not part of the given csv file.
            Converts string values to numeric data as appropriate.
            All file rows must have all columns.
        """
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            num_cols = len(self.columns())
            for row in reader:
                row_cols = len(row)                
                if num_cols != row_cols:
                    raise ValueError(f'expecting {num_cols}, found {row_cols}')
                converted_row = []
                for value in row:
                    converted_row.append(DataTable.convert_numeric(value.strip()))
                self.__row_data.append(DataRow(self.columns(), converted_row))

                    
    def save(self, filename, delimiter=','):
        """Saves the current table to the given file.
        
        Args:
            filename: The name of the file to write to.
            delimiter: The column delimiter to use. 

        Notes:
            File is overwritten if already exists. 
            Table header not included in file output.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)
            for row in self.__row_data:
                writer.writerow(row.values())


    def column_count(self):
        """Returns the number of columns in the data table."""
        return len(self.__columns)


    def row_count(self):
        """Returns the number of rows in the data table."""
        return len(self.__row_data)


    def columns(self):
        """Returns a list of the column names of the data table."""
        return self.__columns.copy()


    def append(self, row_values):
        """Adds a new row to the end of the current table. 

        Args:
            row_data: The row to add as a list of values.
        
        Notes:
            The row must have one value per column. 
        """
        if len(row_values) != len(self.__columns):
            raise ValueError('row must have one value per column')
        self.__row_data.append(DataRow(self.columns(), row_values))
        

    
    def rows(self, row_indexes):
        """Returns a new data table with the given list of row indexes. 

        Args:
            row_indexes: A list of row indexes to copy into new table.
        
        Notes: 
            New data table has the same column names as current table.

        """
        new = DataTable(self.__columns)
        for i in range(len(row_indexes)):
            new.append(self.__row_data[row_indexes[i]].values())
        return new
        

    
    def copy(self):
        """Returns a copy of the current table."""
        table = DataTable(self.columns())
        for row in self:
            table.append(row.values())
        return table
    

    def update(self, row_index, column, new_value):
        """Changes a column value in a specific row of the current table.

        Args:
            row_index: The index of the row to update.
            column: The name of the column whose value is being updated.
            new_value: The row's new value of the column.

        Notes:
            The row index and column name must be valid. 

        """
        if row_index > len(self.__row_data):
            raise IndexError('row index must be valid')
        if column not in set(self.__columns):
            raise IndexError('column name must be valid')
        self.__row_data[row_index][column] = new_value
    

    @staticmethod
    def combine(table1, table2, columns=[], non_matches=False):
        """Returns a new data table holding the result of combining table 1 and 2.

        Args:
            table1: First data table to be combined.
            table2: Second data table to be combined.
            columns: List of column names to combine on.
            nonmatches: Include non matches in answer.

        Notes:
            If columns to combine on are empty, performs all combinations.
            Column names to combine are must be in both tables.
            Duplicate column names removed from table2 portion of result.

        """
        # TODO
        if len(set(columns)) != len(columns):
            raise IndexError("column names must be unique")
        for col in columns:
            if col not in table1.columns() or col not in table2.columns():
                raise IndexError("column name must be included in tables")
        
        # create the list of column names for the new data table
        new_columns = table1.columns()
        for q in table2.columns():
            if q not in new_columns:
                new_columns.append(q)

        new_table = DataTable(new_columns)
        
        # find the overlapping columns if it was not submitted with the function
        #if columns == []:
        #    for m in range(len(table1.columns())):
        #       for n in range(len(table2.columns())):
        #            if table1.columns()[m] == table2.columns()[n]:
        #                columns.append(table1.columns()[m])

        # if columns == [] then every row gets matched to every row

        new_t2_col = []
        for col in table2.columns():
            if col not in columns:
                new_t2_col.append(col)
    
        # no non matches only
        for r1 in table1:
            found = False
            for r2 in  table2:
                if r1.select(columns) == r2.select(columns):
                    found = True
                    new_table.append(r1.values() + r2.select(new_t2_col).values())
            if not found and non_matches:
                new_table.append(r1.values() + ['' for col in new_t2_col])

        for r2 in table2:
            found = False
            for r1 in  table1:
                if r1.select(columns) == r2.select(columns):
                    found = True
            if not found and non_matches:
                tmp_vals = ['' if col not in columns else r2[col] for col in table1.columns()]
                tmp_vals += [r2[col] for col in new_t2_col]
                new_table.append(tmp_vals)
        
       
       
       
        """ # if columns contains all matching columns
        match_col = []
        for m in range(len(table1.columns())):
                if table1.columns()[m] in table2.columns():
                    match_col.append(table1.columns()[m])
        
        if set(columns) == set(match_col):
            # insert all data into new table
            # for table 1
            r = 0
            for row in table1:
                new_row = []
                for col in columns:
                    if col in row.columns():
                        new_row.append(table1[r][col])
                    else:
                        new_row.append('')
                r += 1
                new.append(new_row)

            # table 2
            r = 0
            for row in table2:
                new_row = []
                for col in new_columns:
                    if col in row.columns():
                        new_row.append(table2[r][col])
                    else:
                        new_row.append('')
                r += 1
                new.append(new_row)
            
            
            #replace '' with value if the merging columns have the same values
            # traverse through each value of each row. if the value is not '', continue. if it is '', then: 
            # traverse down each row, comparing the values of the merging columns, 
            # if the values are the same, then replace the og '' with the value in that column of the newly found row. break. 
            for row in new:
                for col in new.columns():
                    if row[col] == '':
                        for rrow in new:
                            match = True
                            for ccol in match_col:
                                if row[ccol] != rrow[ccol]:
                                    match = False
                            if match and rrow[col] != '':
                                row[col] = rrow[col]
            #delete repeat rows:
            # traverse through each row. at each row, traverse through the rest of the table. 
            # if all of the values of the row are equal, then delete the second row. 
            
            
            n = 0
            for row in new:
                n += 1
                for rplace in range(new.row_count()-1):
                    if rplace >= n:  # if we are at a row lower than the row we are checking for
                        match = True
                        for col in new.columns():   
                            if row[col] != new[rplace][col]:
                                match = False
                        if match:
                            # to delete row
                            yrows = []
                            for r in range(new.row_count()):
                                if r != rplace:
                                    yrows.append(r)
                            new = new.rows(yrows)
                            rplace -= 1
           

           
            # if we include non_matches, we are done. If non_matches is False, we must: 
            # traverse through the each element in each row. if an element is == '', then we delete the row
            if non_matches == False:
                row_index = 0
                total = new.row_count()
                while row_index < total:
                    for col in new.columns():
                        delete = False
                        if new[row_index][col] == '': 
                            # delete the row
                            yrows = []
                            for r in range(new.row_count()):
                                if r != row_index:
                                    yrows.append(r)
                            new = new.rows(yrows)
                            total -= 1
                            delete = True
                            break
                    if delete == False:
                        row_index += 1

         """


        return new_table
        

    
    @staticmethod
    def convert_numeric(value):
        """Returns a version of value as its corresponding numeric (int or
        float) type as appropriate.

        Args:
            value: The string value to convert

        Notes:
            If value is not a string, the value is returned.
            If value cannot be converted to int or float, it is returned.

         """
        try:        
            int_val = int(value)
            return int_val
        except:
            try:
                flo_val = float(value)
                return flo_val
            except:
                return value
    
