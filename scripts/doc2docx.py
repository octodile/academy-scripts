# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0703,R0903
""" Allows you to convert a Microsoft Word DOC format to DOCX document
"""

# --------------------------- REQUIRED LIBRARIES ------------------------------

import argparse
import os
import win32com.client


# -------------------------- MAIN SCRIPT BEHAVIOR -----------------------------


class App(object):
    """ Application main controller, this class has been defined following the
    singleton pattern to ensures only one object can be instantiated.
    """

    __instance = None

    def __new__(cls):
        """ Prevent multiple instances from self (Singleton Pattern)
        """

        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.name = "The one"
        return cls.__instance

    def __init__(self):
        self.abspath = None
        self.basename = None
        self.dirname = None
        self.filename = None

    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        description = u'Convert a Microsoft Word DOC format to DOCX document.'

        parser = argparse.ArgumentParser(description)
        parser.add_argument('file', metavar='file', type=str,
                            help='path of the .docx file will be converted')

        args = parser.parse_args()

        self.abspath = os.path.abspath(args.file)
        self.basename = os.path.basename(self.abspath)
        self.dirname = os.path.dirname(self.abspath)
        self.filename = self.basename and os.path.splitext(self.basename)[0]

    def _doc2docx(self):
        """ Performs the conversion from doc to docx
        """

        new_path = os.path.join(self.dirname, self.filename+'.docx')

        try:

            word = win32com.client.DispatchEx("Word.Application")
            doc = word.Documents.Open(self.abspath)
            doc.SaveAs(new_path, FileFormat=12)

            doc.Close()
            word.Quit()

        except Exception as ex:
            print ex
        else:
            print u'New file %s has been written.' % new_path

    def _is_file(self):
        """ Check if given path is a valid file path
        """
        return os.path.isfile(self.abspath)

    def main(self):
        """ The main application behavior, this method should be used to
        start the application.
        """

        self._argparse()
        if self._is_file():
            self._doc2docx()


# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()
