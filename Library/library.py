import pandas as pd 
import string

def library():
    df = pd.read_csv(r"C:\Users\kloke\OneDrive\Desktop\UoSM\SEM1\33\python\bookdata.csv")

    print("\n--> Welcome To The Library <--\n") 
    print(" -- How can I help you? -- ")
    print("Press the digit and Enter:")
    print("[1] to ADD a book") 
    print("[2] to EDIT a book's information")
    print("[3] to DELETE a book")
    print("[4] to check a book's AVAILABILITY")
    print("[5] to SEARCH for a book\n")

    choices = (1, 2, 3, 4, 5) 
    while True:
        option = input("Input Number Here: ") # User needs to input the number based on what they want to do
        if not option.isdigit():
            print("Please Input A Number!") # error handles if the inputted is not a number
            continue

        option = int(option)
        if option not in choices: # error handles if the inputted is a number but not within the range
            print("That is not a valid input")
        else:
            break

    if (option == 1):
        print(">> ADD BOOKS <<") # Section Name will be displayed
        print('\n')

        Title = input("Book Title: ") # Name of the Book to add
        Author = input("Author: ") # the author of the book
        ISBN = input("ISBN: ") # the ISBN
        while not ISBN.isdigit(): # to make sure the input are numbers and not characters or anything else
            print("Only Numbers are Accepted")
            ISBN = input("ISBN: ")
            while (len(ISBN) < 13 or len(ISBN) > 13): # the standard ISBN has 13 digits only
                if (len(ISBN) < 13):
                    print("You seem to be missing a few digits") # a message if the length of the ISBN is lesser than 13 digits
                if (len(ISBN) > 13):
                    print("You seem to have too many digits") # a message if the length of the ISBN is more than 13 digits
                ISBN = input("ISBN: ")

        Genre = input("Genre: ") # the genre of the book

        Year = int(input("Publication Year: ")) # the year the book was published
        while(Year > 2023 or Year < 800): # checks to make sure the book was published within the valid publishing period
            if (Year > 2023):
                print("2023 has not even passed yet!")
            elif (Year < 800):
                print("We aren't dinosaurs!") # the first earliest to data book published was in the year 800
            Year = int(input("Publication Year: "))

        Language = input("Language: ").capitalize() # the book's language, capitalised to make it easier for the database
        Series = input("Series (put '-' if the book does not belong to any series): ") # if the book is part of a series
        Qty = input("Book Quantity: ") # the quantity of books that the User is adding 
        Available = input("Available? (Yes/No): ").capitalize() 
        while Available not in ['Yes', 'No']:
            print("Please State either Yes or No")
            Available = input("Available? (Yes/No): ").capitalize()

        new_data = { # Labelling which of the database's header does each newly added data belong to
            "Title": [Title],
            "Author": [Author],
            "ISBN": [ISBN],
            "Genre": [Genre],
            "Publication Year": [Year],
            "Language": [Language],
            "Series": [Series],
            "Qty": [Qty],
            "Available?": [Available]
        }

        df = pd.DataFrame(new_data) # creating a new data frame for the newly added data

        # Updating the database by appending it, not updating the index and making sure the header does not get modified
        df.to_csv("C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM1\\33\\python\\bookdata.csv", mode='a', index=False, header=False)

        # a message to show that the book has been appended to the database
        print("Book has been succesfully added!")


    if (option == 2):
        print(">> EDIT BOOK <<")

        print(df) # prints the database for the User to reference from
        print('\n')
        
        max_rows = len(df) # assigning the number of rows that the databse has to max_rows
        row = int(input("Which Row do would you like to Edit? ")) # asks the User which row from the printed database he wants to edit
        while (row < 0 or row > len(df)): # error handling incase the User enters a row number that is 
                                          # non existant or exceeds the number of rows the database actually has
            print(f"You have to choose between 0 to {max_rows - 1} rows!") # -1 because the system counts from 0
            row = int(input("Which Row do would you like to Edit? ")) # the row number where the book is located

        column = (input("Under which header? ")) # what detail of the book is to be edited
        while (column not in df.columns): # error handling incase a header that does not exist is chosen
            print("I'm afriad that header does not exist D:")
            column = (input("Under which header? "))

        new_value = (input("Modified Information: ")) # the info to replace the original

        value = df.loc[row, column] # storing the book's row's data
        print(f"\nValue Chosen to be Changed at ({row}, '{column}'): {value}") # confirms that the data chosen to be edited is correct
        confirm = input("Confirm Changes for this cell? (yes/no): ").lower() # confirms to change the data
        if (confirm == 'yes'):
            df.loc[row, column] = new_value # the book's value in that column is replaced with the new data
            df.to_csv("C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM1\\33\\python\\bookdata.csv", index=False) # database is updated
            print('\n')
            print(df)
            print('\n')
            print(">> Modification Successful! <<")

        elif (confirm == 'no'):
            print(">> No Modifications were made <<")


    if (option == 3):
        print(">> DELETE BOOK <<")

        print(df)
        print('\n')

        DelRow = int(input("Which Book Row Would You Like to Delete? ")) # asks the User which book data he wants to delete
        max_rows = len(df)
        while(DelRow < 0 or DelRow > max_rows):
            print(f"You have to choose between 0 to {max_rows - 1} rows!")
            DelRow = int(input("Which Book Row Would You Like to Delete? "))

        row_data = df.loc[DelRow] # stores the book's row data
        print(f"\nBook Row chosen to be Deleted: {DelRow}\n{row_data}") # displays the to-be-deleted book's data
        choices = ('yes', 'no')
        confirm = input("Confirm to Delete this Book Row? (yes/no): ").lower()
        while(confirm not in choices):
            print("Please State yes OR No :'D")
            confirm = input("Confirm to Delete this Book Row? (yes/no): ").lower()
        if (confirm == 'yes'):
            df = df.drop(df.index[DelRow]) # deletes the book's data
            df.to_csv("C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM1\\33\\python\\bookdata.csv", index=False) # updates the database
            print(df)
            print('\n')
            print("Book Row has been Deleted!")
        if (confirm == 'no'):
            print("Nothing has been Deleted")


    if (option == 4):
        print(">> AVAILABILITY <<")
        print('\n')

        book_title = input("Which Book Would You Like to Search For? ") # asks the User to type the book's name

        case_insensitive_book_title = book_title.lower().translate(str.maketrans("", "", string.punctuation))
        # makes the inputted book name all lower case with its punctuations removed
        # and then stores the translated book title to another variable for easy comparison and location
        result = df[df['Title'].str.lower().str.translate(str.maketrans("", "", string.punctuation)) == case_insensitive_book_title]
        # translates the database's original book names and compares it with the new variable

        print("\nSearch Result:")
        if result.empty:
            print("We do not seem to have that book :(")
        else:
            print(result[['Title', 'ISBN', 'Qty', 'Available?']]) # displays only certain properties of the book
        print('\n')

        for index, book_name in result.iterrows(): # goes through the database to find out whether it is available to loan
            if (book_name['Available?'] == 'Yes'):
                print("This Book is Available!")
                Loan = input("Would You Like to Loan this Book? (yes/no): ").lower()
                if (Loan == 'yes'):
                    df.at[index, 'Qty'] -= 1 # decreaments the qty of the said book by 1
                    if (df.at[index, 'Qty'] == 0): # changes the availability to no if the qty reaches 0
                        df.at[index, 'Available?'] = 'No'
                    df.to_csv(r"C:\\Users\\kloke\\OneDrive\\Desktop\\UoSM\\SEM1\\33\\python\\bookdata.csv", index=False)
                    print(f"You Have Now Loaned {book_name['Title']}!")

                    if (Loan == 'no'):
                        print("Come Back Next Time!")

                    if (book_name['Available?'] == 'No'):
                     print("Unfortunately, this book is currently being loaned")


    if (option == 5):
        print("SEARCH BOOK")
        print("\n")

        print("What Category Would You Like To Search By? ")
        categories = ('title', 'author', 'isbn', 'genre', 'publication year', 'language', 'series', 'availability')
        print("Choose From One of the Following: Title, Author, ISBN, Genre, Publication Year, Language, Series, Availability")
        category_chosen = input("Category: ").lower() # made lower case for user-friendliness
        while (category_chosen not in categories):
            print("That is not a Category available")
            category_chosen = input("Category: ").lower()

        def searching(category, input_category): # function to make the intended search to be incase sensitive
            search = input(input_category)

            case_insensitive_search = search.lower().translate(str.maketrans("", "", string.punctuation))
            result = df[df[category].str.lower().str.translate(str.maketrans("", "", string.punctuation)) == case_insensitive_search]

            if result.empty:
                print("\nSearch Results:")
                print(">> No Results Found ): <<\n")
            else:
                print("\nSearch Results:")
                print(result)
                print('\n')

        def searching_nb(category, input_category): # function to search properties that are integers
            search = input(input_category)

            if category.lower() in ['isbn', 'publication year']:
                try:
                    search = int(search)
                except ValueError:
                    print("Please Enter The Right Combination of Digits")
                    return
                
            result = df[df[category] == search]

            if result.empty:
                print("\nSearch Results:")
                print(">> No Results Found ): <<\n")
            else:
                print("\nSearch Results:")
                print(result)
                print('\n')

        if (category_chosen == 'title'):
            searching('Title', "Book Title: ")

        if (category_chosen == 'author'):
            searching('Author', "Author: ")

        if (category_chosen == 'isbn'):
            searching_nb('ISBN', "ISBN: ")

        if (category_chosen == 'genre'):
            searching('Genre', "Genre: ")

        if (category_chosen == 'publication year'):
            searching_nb('Publication Year', "Publication Year: ")

        if (category_chosen == 'language'):
            searching('Language', "Language: ")

        if (category_chosen == 'series'):
            searching('Series', "Series: ")

        if (category_chosen == 'availability'):
            searching('Available?', "Availability? (Yes/No): ")

library() # for the library function to run automatically upon running

print("Thank You For Visiting The Library!")
leaving = input("Would You Like To Do Anything Else? (y/n): ").lower() # asks the User whether he wants to continue
if (leaving == 'y'):
    library()
if (leaving == 'n'):
    print("See You Next Time!")
while (leaving not in ['y', 'n']):
    print("You Gotta Choose!")
    leaving = input("Would You Like To Do Anything Else? (y/n): ").lower()