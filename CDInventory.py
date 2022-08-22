#-------------------------------------------------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# qinlaura, 2022-Aug-14, Updated File
# qinlaura, 2022-Aug-21, Updated script to use binary file and added error handling
#-------------------------------------------------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #

class DataProcessor:
    '''Processing the data stored in memory'''

    @staticmethod
    def add_row_to_data(id, title, artist, table):
        '''Function to add a new row of data to the table in memory

        Taking the id, title and artist entered by the user, turn it into a dictionary and append it to 
        the table in memory.

        Args:
            id (string): the id of the new row
            title (string): the title of the cd
            artist (string): the artist of the cd
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        '''
        int_id = int(id)
        dicRow = {'ID': int_id, 'Title': title, 'Artist': artist}
        table.append(dicRow)

    @staticmethod
    def delete_row(delete_id, table):
        '''Function to delete a row from the table in memory

        Taking the id of the row the user wants to delete, search through the table in memory, 
        check each row to see if the id matches the id of the row that the user wants to delete,
        and remove that row from the table.

        Args:
            delete_id (string): the id of the row that user wants to delete
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        '''
        int_delete_id = int(delete_id)
        row_num = -1
        cd_removed = False
        for row in table:
            row_num += 1
            if row['ID'] == int_delete_id:
                del table[row_num]
                cd_removed = True
                break
        if cd_removed:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    '''Processing the data to and from text file'''

    @staticmethod
    def read_file(file_name):
        '''Function to manage data ingestion from file to a list of dictionaries

        Reads the data from the pickle file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data
        '''
        with open(file_name, 'rb') as obj_file:
            table = pickle.load(obj_file)
        return table

    @staticmethod
    def write_file(file_name, table):
        '''Function to save the table in memory into the file

        Write the data that is a 2D list of dictionaries into a pickle file

        Args:
            file_name (string): name of file to save data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        '''

        with open(file_name, 'wb') as obj_file:
            pickle.dump(table, obj_file)

# -- PRESENTATION (Input/Output) -- #

class IO:
    '''Handling Input / Output'''

    @staticmethod
    def print_menu():
        '''Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        '''

        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        '''Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        '''
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def get_input_row():
        '''Gets user input for a new row of data

        Prompts the user to enter the id, title and artist for a new row of data, and then store the entered values
        into three seperate string variables

        Args:
            None.

        Returns:
            id, title, artist (a tuple of strings): the id, title and artist entered by a user, stored in strings
            inside a tuple
        '''
        id = input('Enter ID: ').strip()
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        return id, title, artist

    @staticmethod
    def show_inventory(table):
        '''Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        '''
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def get_reload_yes_no():
        '''Ask user to confirm if they want to reload data, save user entry in a string

        Prints out a warning that says if the user procees to reload data from file, all unsaved changes in
        memory will be discarded. Then it asks user to confirm they want to proceed by typing in 'yes',
        otherwise abort the reload.

        Args:
            None.

        Returns:
            reload_yes_no (string): whether or not user wants to proceed with reloading data
        '''
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        reload_yes_no = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        return reload_yes_no

    @staticmethod
    def get_delete_id():
        '''Ask user to enter the id of the row they would like to delete, and store it in a string

        Args:
            None.

        Returns:
            del_id (string): the id of the row to be deleted from the table
        '''    
        del_id = input('Which ID would you like to delete? ').strip()
        return del_id

    @staticmethod
    def get_save_yes_no():
        '''Ask user to whether they want to save the current inventory to file, and store it in a string

        Args:
            None.

        Returns:
            save_yes_no (string): whether or not the user wants to save current inventory to file
        '''    
        save_yes_no = input('Save this inventory to file? [y/n] ').strip().lower()
        return save_yes_no



# 1. When program starts, read in the currently saved Inventory
try:
    lstTbl = FileProcessor.read_file(strFileName)
except FileNotFoundError as e:
    print('\nInventory data file does not exist')
    print('Detailed error message: ')
    print(type(e), e, e.__doc__, sep = '\n')

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        try:
            strYesNo = IO.get_reload_yes_no()
            if strYesNo.lower() == 'yes':
                print('reloading...\n')
                lstTbl = FileProcessor.read_file(strFileName)
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except FileNotFoundError as e:
            print('\nInventory data file does not exist')
            print('Detailed error message: ')
            print(type(e), e, e.__doc__, sep = '\n')
        except Exception as e:
            print('\nThere was a general error')
            print('Detailed error message: ')
            print(type(e), e, e.__doc__, sep = '\n')
    # 3.3 process add a CD
    elif strChoice == 'a':
        try:
            # 3.3.1 Ask user for new ID, CD Title and Artist
            strID, strTitle, strArtist = IO.get_input_row()
            # 3.3.2 Add item to the table
            DataProcessor.add_row_to_data(strID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError as e:
            print('\nInvalid ID, needs to be an integer')
            print('Detailed error message: ')
            print(type(e), e, e.__doc__, sep = '\n')
        except Exception as e:
            print('\nThere was a general error')
            print('Detailed error message: ')
            print(type(e), e, e.__doc__, sep = '\n')
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        try:
            # 3.5.1 get Userinput for which CD to delete
            # 3.5.1.1 display Inventory to user
            IO.show_inventory(lstTbl)
            # 3.5.1.2 ask user which ID to remove
            intIDDel = IO.get_delete_id()
            # 3.5.2 search thru table and delete CD
            DataProcessor.delete_row(intIDDel, lstTbl)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError as e:
            print('\nInvalid ID, needs to be an integer')
            print('Detailed error message: ')
            print(type(e), e, e.__doc__, sep = '\n')
        except Exception as e:
            print('\nThere was a general error')
            print('Detailed error message: ')
            print(type(e), e, e.__doc__, sep = '\n')
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = IO.get_save_yes_no()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
