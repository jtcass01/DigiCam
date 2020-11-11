#!/usr/bin/env python
"""FileSystem.py: Module containing a wrapper class for accessing and modifying directories and files."""

__author__ = "Jacob Taylor Cassady"
__email__ = "jacobtaylorcassady@outlook.com"

from os.path import isdir, exists
from shutil import rmtree
from os import walk, rename, makedirs
from typing import Union, Any
from datetime import datetime


class FileSystem():
    """Class Object to handle the querying of File Directories information regarding the files within."""
    ## STATIC METHODS
    @staticmethod
    def get_files(directory_location: str) -> set:
        """Retrieves a set of files from the FileSystem's target directory attribute.

        Args:
            directory_location (str): [description]

        Returns:
            set: [description]"""
        file_set = list([])

        # If the directory exists, return the set of files found within. Else print a warning that the directory does not exist.
        if isdir(directory_location):
            for root, dirs, files in walk(directory_location):
                file_set.append(set(files))

        # If no files are found or the directory does not exist, return the empty set.
        return set(file_set)

    @staticmethod
    def get_new_files(directory_location: str, current_files: Union[list, set]) -> list:
        """Retrieves a list of files added to the FileSystem's target directory as compared to it's current attribute set of files_found

        Args:
            directory_location (str): [description]
            current_files (Union[list, set]): [description]

        Returns:
            list: [description]"""
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
    def log(data: Any, file_name: str) -> None:
        """Logs the data to the location [file_name].

        Args:
            data (Any): [description]
            file_name (str): [description]"""
        try:
            with open(file_name, "a+") as file:
                file.write(str(data) + "\n")
        except PermissionError:
            print("Permission error when accessing file: " + file_name)

    @staticmethod
    def log_by_timestamp(data: Any, file_name: str, timestamp_delimiter: str = "\t"):
        """Timestamps data and logs it to the file_name.

        Args:
            data (Any): [description]
            file_name (str): [description]
            timestamp_delimiter (str, optional): [description]. Defaults to "\t"."""
        FileSystem.log(data=str(datetime.now()) + timestamp_delimiter + str(data), file_name=file_name)

    @staticmethod
    def move_files(source_dir: str, destination_dir: str, new_name: Union[str, None] = None) -> None:
        """Moves all files from a source directory into a destination directory.  If new_name is not None, the files are 
           renamed and enumerated using the new_name.  If new_name is None, the files keep their original name.

        Args:
            source_dir (str): [description]
            destination_dir (str): [description]
            new_name (Union[str, None], optional): [description]. Defaults to None."""
        # Determine the current size of the destination directory to ensure enumerations don't overlap when renaming files.
        initial_index = 0

        # Set the initial index to the length of files within the destination directory
        for root, dirs, files in walk(destination_dir):
            initial_index = len(files)

        # Get a list of source files.
        source_files = list([])
        for root, dirs, files in walk(source_dir):
            source_files = files

        # Move and rename source files to the destination directory.
        for index, file in enumerate(source_files):
            if new_name is None:
                rename(source_dir + file, destination_dir + file)
            else:
                rename(source_dir + file, destination_dir + new_name + str(index + initial_index) + ".bin")

    @staticmethod
    def start_log(data: Any, file_name: str) -> None:
        """Logs the data to the location [file_name]. Note all previous information contained within this file will be deleted.

        Args:
            data (Any): [description]
            file_name (str): [description]"""
        with open(file_name, "w+") as file:
            file.write(str(data) + "\n")

    @staticmethod
    def enforce_path(purposed_path: str) -> None:
        """Ensures a directory path exists.

        Args:
            purposed_path (str): [description]"""
        makedirs(purposed_path, exist_ok=True)

    @staticmethod
    def delete_directory(directory: str) -> None:
        """Deletes a directory if it exists.

        Args:
            directory (str): [description]"""
        if exists(directory):
            rmtree(directory)

    @staticmethod
    def log_error(error: Union[Exception, str], file_name: str, timestamp_delimeter="\t") -> None:
        """Logs an error with a timestamp using a given delimeter and file_name

        Args:
            error (Union[Exception, str]): [description]
            file_name (str): [description]
            timestamp_delimeter (str, optional): [description]. Defaults to "\t"."""
        FileSystem.log_by_timestamp(data=error, timestamp_delimeter=timestamp_delimeter, file_name=file_name)

    @staticmethod
    def initialize_csv(directory_location: str, file_name: str, column_headers: list, delimeter: str) -> None:
        """Initializes a csv file with a given list of column headers

        Args:
            directory_location (str): [description]
            file_name (str): [description]
            column_headers (list): [description]
            delimeter (str): [description]"""
        # Enforce the directory path
        FileSystem.enforce_path(purposed_path=directory_location)
        # Start the log with the correct delimeter information at the top
        FileSystem.start_log(data="sep=" + delimeter, file_name=directory_location+file_name)
        # Add the column headers to the log.
        FileSystem.log(data=delimeter.join(column_headers), file_name=directory_location+file_name)
