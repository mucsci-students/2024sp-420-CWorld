from .controller_input import read_file, read_line
import umleditor.mvc_controller.controller_output as controller_output
from umleditor.mvc_controller.uml_parser import Parser
from .serializer import CustomJSONEncoder, serialize, deserialize
from umleditor.mvc_model import CustomExceptions as CE
from umleditor.mvc_model.diagram import Diagram
from umleditor.mvc_model import help_menu
from umleditor.mvc_controller.uml_parser import check_args
import os

#Parser Includes. These will be moved out when the parser is moved.
from umleditor.mvc_model.entity import Entity
from umleditor.mvc_model.relation import Relation




class Controller:
    def __init__(self) -> None:
        self._should_quit = False
        self._diagram = Diagram()

    
    def run(self) -> None:
        while not self._should_quit:
            s = read_line()
            p = Parser(self._diagram)
            try:
                #parse the command
                input = p.parse(s)

                #return from input is [function object, arg1,...,argn]
                command = input[0]
                args = input[1:]

                #execute the command
                out = command(*args)

                #write output if it was something
                if out != None:
                    controller_output.write(out)
            
            except TypeError as t:
                controller_output.write(CE.InvalidArgCountError(t))
            except ValueError as v:
                controller_output.write(CE.NeedsMoreInput())
            except Exception as e:
                controller_output.write(str(e))
            
    def quit(self):
        '''Basic Quit Routine. Prompts user to save, where to save, 
            validates input.
            
        Returns:
            If the name and filepath were valid or user doesn't want to save, returns true
            If name is invalid, returns invalid filename exception
            If filepath is invalid, returns invalid filepath exception
        '''
        self._should_quit = True
        while True:
            answer = read_line('Would you like to save before quit? [Y]/n: ').strip()
            if not answer or answer in ['Y', 'n']: # default or Y/n
                break
        if answer == 'n':
            #user wants to quit without saving
            return
        else:
            answer = read_line('Name of file to save: ')

        if isinstance(check_args([answer]), Exception):
            return CE.IOFailedError("Save", "invalid filename")

        self.save(answer)

    def save(self, name: str) -> None:
        '''
        Saves the current diagram using a serializer with the given filename

        #### Parameters:
        - `name` (str): The name of the file to be saved.
        '''
        path = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        serialize(diagram=self._diagram, path=path)

    def load(self, name: str) -> None:
        '''
        Loads a diagram with the given filename using a deserializer.

        #### Parameters:
        - `path` (str): The name of the file to be loaded.
        '''
        path = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        loadedDiagram = Diagram()
        deserialize(diagram=loadedDiagram, path=path)
        self._diagram = loadedDiagram
    
