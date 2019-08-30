"""
Module Description:
Module containing a wrapper class for accessing and modifying directories and files.

Author:
Jacob Taylor Cassady

Dates:
Last Updated - 6/25/18
"""

# Built-in modules
## Operating System module
import os, shutil, datetime

class FileSystem():
    """
    Class Description:
    Class Object to handle the querying of File Directories information regarding the files within.

    Author:
    Jacob Taylor Cassady
    """
    ## STATIC METHODS
    @staticmethod
    def get_files(directory_location):
        """
        Function Description:
        Retrieves a set of files from the FileSystem's target directory attribute.
        
        Author:
        Jacob Taylor Cassady
        """
        file_set = set([])

        # If the directory exists, return the set of files found within. Else print a warning that the directory does not exist.
        if os.path.isdir(directory_location):
            for root, dirs, files in os.walk(directory_location):
                files = set(file_set)

        # If no files are found or the directory does not exist, return the empty set.
        return file_set

    @staticmethod
    def get_new_files(directory_location, current_files):
        """
        Function Description:
        Retrieves a list of files added to the FileSystem's target directory as compared to it's current attribute set of files_found

        Author:
        Jacob Taylor Cassady
        """
        files = FileSystem.get_files(directory_location)

        # If there are files within the directory continue, if not return the empty list.
        if files is not None:
            # Find the difference in the new files found set to the current set of files
            new_files = files - current_files

            # Return the difference cast to a list.  If empty, return an empty list
            if len(new_files) > 0:
                return list(new_files)
            else:
                return list([])
        else:
            return list([])

    @staticmethod
    def log(data, file_name):
        """
        Function Description:
        Logs the data to the location [file_name]. Note all previous information contained within this file will be deleted.

        Author:
        Jacob Taylor Cassady
        """
        try:
            with open(file_name, "a+") as file:
                file.write(data + "\n")

        except PermissionError:
            print("Permission error when accessing file: " + file_name)

    @staticmethod
    def log_by_timestamp(data, file_name, delimiter="\t"):
        """
        Function Description:
        Timestamps data and logs it to the file_name.

        Author:
        Jacob Taylor Cassady
        """
        FileSystem.log(data=str(datetime.datetime.now()) + delimiter + data, file_name=file_name)

    @staticmethod
    def move_files(source_dir, destination_dir, new_name = None):
        """
        Function Description:
        Moves all files from a source directory into a destination directory.  If new_name is not None, the files are renamed and enumerated using the
        new_name.  If new_name is None, the files keep their original name.

        Author:
        Jacob Taylor Cassady
        """
        # Determine the current size of the destination directory to ensure enumerations don't overlap when renaming files.
        initial_index = 0

        # Set the initial index to the length of files within the destination directory
        for root, dirs, files in os.walk(destination_dir):
            initial_index = len(files)

        # Get a list of source files.
        source_files = list([])
        for root, dirs, files in os.walk(source_dir):
            source_files = files

        # Move and rename source files to the destination directory.
        for index, file in enumerate(source_files):
            if new_name is None:
                os.rename(source_dir + file, destination_dir + file)
            else:
                os.rename(source_dir + file, destination_dir + new_name + str(index + initial_index) + ".bin")

    @staticmethod
    def start_log(data, file_name):
        """
        Function Description:
        Logs the data to the location [file_name]. Note all previous information contained within this file will be deleted.

        Author:
        Jacob Taylor Cassady
        """
        with open(file_name, "w+") as file:
            file.write(data + "\n")

    @staticmethod
    def enforce_path(purposed_path):
        """
        Function Description:
        Ensures a directory path exists.

        Author:
        Jacob Taylor Cassady
        """
        if not os.path.exists(purposed_path):
            os.makedirs(purposed_path)

    @staticmethod
    def delete_directory(directory):
        """
        Function Description:
        Deletes a directory if it exists.

        Author:
        Jacob Taylor Cassady
        """
        if os.path.exists(directory):
            shutil.rmtree(directory)

    @staticmethod
    def log_error(error, file_name, delimeter="\t"):
        """
        Function Description:
        Logs an error with a timestamp using a given delimeter and file_name

        Author:
        Jacob Taylor Cassady
        """
        FileSystem.log_by_timestamp(data=error, delimiter=delimeter, file_name=file_name)

    @staticmethod
    def initialize_csv(directory_location, file_name, column_headers, delimeter):
        """
        Function Description:
        Initializes a csv file with a given delimeter 

        Author:
        Jacob Taylor Cassady
        """
        # Enforce the directory path
        FileSystem.enforce_path(purposed_path=directory_location)
        # Start the log with the correct delimeter information at the top
        FileSystem.start_log(data="sep=" + delimeter, file_name=directory_location+file_name)
        # Add the column headers to the log.
        FileSystem.log(data=delimeter.join(column_headers), file_name=directory_location+file_name)
