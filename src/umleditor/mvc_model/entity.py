# Primary: Danish
# Secondary: Zhang
from .custom_exceptions import CustomExceptions
from typing import Optional

class Entity:

    def __init__(self, entity_name: str = ''):
        """
        Constructs a new Entity object.

        Args:
            entity_name (str): The name of the entity.
        """
        self._name: str = entity_name
        self._fields: list[tuple[str, type]] = []
        self.allowed_types = {
            "string": str,
            "int": int,
            "bool": bool,
            "float": float
        }
        self._methods = []
        self.allowed_return_types = {
            "void": None, 
            "string": str,
            "int": int,
            "bool": bool,
            "float": float
            }

    def get_name(self):
        """
        Returns the name of the entity.

        # Returns:
            (str): The name of the entity
        """
        return self._name

    def set_name(self, entity_name: str):
        """
        Update entity name.

        Args:
            entity_name (str): The new name for the entity.
        """
        self._name = entity_name

    def add_field(self, field_name: str, field_type: type):
        """
        Adds a new field to the to the list.

        Args:
            field_name (str): The field' name to be added to the entity.
            field_type (type): The field type to be added to the entity.

        Raises:
            CustomExceptions.FieldExistsError: If the field already
                exists in the Entity.

        Returns:
            None.
        """
        if field_name in self._fields:
            raise CustomExceptions.FieldExistsError(field_name)

        else:
            if field_type not in self.allowed_types:
                raise CustomExceptions.FieldtypeNotFoundError(field_type)

            else:
                if isinstance(field_type, str):
                    field_type = self.allowed_types[field_type]
                self._fields.append((field_name, field_type))

    def delete_field(self, field_name: str,field_type: str):
        """
        Deletes a field from this entity if the field exists.

        Args:
            field_name (str): The name of the field to be deleted from the entity.
            field_type (type): The type of the field to be deleted from the entity.

        Raises:
            CustomExceptions.FieldNotFoundError: If the specified field
                is not found in the entity's field list.

        Returns:
            None.
        """
        field_found = False
        for field in self._fields:
            if field[0] == field_name:  # Compare only the field names
                self._fields.remove(field)
                field_found = True
                break

        if not field_found:
            raise CustomExceptions.FieldNotFoundError(field_name)

    def rename_field(self, old_field: str, old_type: type, new_field: str, new_type: type):
        """
        Renames a field from its old name to a new name

        Args:
            old_field(str): The current name of the field.
            old_type(type): The current type of the field.
            new_field (str): The new name for the field.
            new_type (type): The new type for the field.

        Raises:
            CustomExceptions.FieldNotFoundError: If the old field does
                not exist in the entity.
            CustomExceptions.FieldExistsError: If the new name is already
                used for another field in this entity.

        Returns:
            None.
        """

        if any(field[0] == new_field for field in self._fields):
            raise CustomExceptions.FieldExistsError(new_field)

        field_found = False

        for index, (field_name, field_type) in enumerate(self._fields):
            if field_name == old_field and field_type == old_type:
                self._fields[index] = (new_field, new_type)
                field_found = True
                break

        if not field_found:
            raise CustomExceptions.FieldNotFoundError(old_field)

    def get_method(self, method_name: str):
        """
        Checks if a method exists inside an entity.

        Args:
            method_name (str): The method's name to be checked for.

        Raises:
            None.

        Returns:
            UML_Method: Returns method if it exists
        """
        for m in self._methods:
            if m.get_method_name() == method_name:
                return m
        raise CustomExceptions.MethodNotFoundError(method_name)

    def add_method(self, method_name: str, return_type: str):
        """
        Adds a new method to the to the list.

        Args:
            method_name (str): The method's name to be added to the entity.
            return_type (type): The method's return type to be added to the entity.

        Raises:
            CustomExceptions.MethodExistsError: If the method already
                exists in the Entity.
        Returns:
            None.
        """
        if any(method_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodExistsError(method_name)
        if return_type not in self.allowed_return_types:
            raise ValueError(f"Invalid return type: {return_type}")

        new_method = UML_Method(method_name, return_type)
        self._methods.append(new_method)

    def add_method_and_params(self, method_name: str, return_type: str, param_name: str, param_type: type):
        """
        Adds a method with specified parameters to the class.

        Parameters:
            method_name (str): The name of the method to add.
        """

        self.add_method(method_name, return_type)
        self.get_method(method_name).add_parameters(param_name, param_type)

    def edit_method(self, old_method: str, new_method: str, return_type: str, param_name: str, param_type: type):
        deleted_method = self.get_method(old_method)
        self.delete_method(old_method)
        try:
            self.add_method_and_params(new_method, return_type, param_name, param_type)
        except Exception as e:
            self._methods.append(deleted_method)
            raise e

    def delete_method(self, method_name: str):
        """
        Deletes a method from this entity if the method exists.

        Args:
            method_name (str): The name of the method to be deleted from the entity.

        Raises:
            CustomExceptions.MethodNotFoundError: If the specified method
                is not found in the entity's method list.

        Returns:
            None.
        """
        if not any(method_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodNotFoundError(method_name)
        for um in self._methods:
            if um.get_method_name() == method_name:
                self._methods.remove(um)

    def rename_method(self, old_name: str, new_name: str):
        """
        Renames a method from its old name to a new name

        Args:
            old_name(str): The current name of the method.
            new_name (str): The new name for the method.

        Raises:
            CustomExceptions.MethodNotFoundError: If the old method does
                not exist in the entity.
            CustomExceptions.MethodExistsError: If the new name is already
                used for another method in this entity.

        Returns:
            None.
        """
        if not any(old_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodNotFoundError(old_name)
        elif any(new_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodExistsError(new_name)
        else:
            for um in self._methods:
                if old_name == um.get_method_name():
                    um.set_method_name(new_name)

    def list_fields(self):
        """Lists all the fields of this entity

            Return: a comma separated list of all methods in this entity
        """
        return ", ".join(f"{name}: {ftype.__name__}" for name, ftype in self._fields)

    def list_methods(self):
        """Lists all the methods of this entity

            Return: a comma separated list of all methods and their params in this entity
        """
        return ", ".join(m.__str__() for m in self._methods)

    def __str__(self) -> str:
        """
        Returns the string representation of the Entity object (its name).

        Returns:
            str: The name of the entity.
        """
        # return_type_name = 'void' if self.allowed_return_types is type(None) else self.allowed_return_types.__name__
        return f"{self._name}: {self.allowed_return_types}"

    def __eq__(self, other):
        """Equality operator for entities

            Return:
            True - this and other have the same name
            False - this and other do not have the same name
        """
        return self._name == other._name


# ====================================================================================#
#                                  Method Definition
# ====================================================================================#


class UML_Method:

    def __init__(self, method_name: str = '', return_type: str = ''):
        """
        Creates a UML_Method object.

        Args:
            method_name (str): The name of the method.
            return_type (type): The Return type of the method.

        Raises:
            None.

        Returns:
            None.
        """
        self._name = method_name
        self._return_type = return_type
        self._params: list[tuple[str, Optional[type]]] = []
        self.allowed_types = {
            "string": str,
            "int": int,
            "bool": bool,
            "float": float
        }

    def get_method_name(self):
        """
        Returns the name of the method.

        Args:
            None.

        Raises:
            None.

        Returns:
            name (Entity): The name of the method.
        """
        return self._name

    def set_method_name(self, new_name):
        """
        Changes the name of the method.

        Args:
            new_name (str): The new name of the method.

        Raises:
            None.

        Returns:
            None.
        """
        self._name = new_name

    def get_return_type(self):
        return self._return_type

    def _check_duplicate_parameters(self, param_name: str):
        """
        Checks if there are duplicate paramters.

        Args:
           param_name: The list of new parameters to be checked.

        Raises:
            CustomExceptions.DuplicateParametersError: If any of the parameter occurs more than once.
        """
        for existing_param_name, _ in self._params:
            if existing_param_name == param_name:
                raise CustomExceptions.ParameterExistsError(param_name)

    def add_parameters(self, param_name: str, param_type: Optional[type] = None):
        """
        Adds a list of new parameters to the method.

        Args:
            param_name: The list of new parameters to be added.
            param_type: The type of new parameters to be added.

        Raises:
            CustomExceptions.ParameterExistsError: If any of the parameter already exists in the method.

        Returns:
            None.
        """
        self._check_duplicate_parameters(param_name)
        self._params.append((param_name, param_type))

    def remove_parameters(self, param_name: str, param_type: type):
        """
        Removes a list of parameters from the method.

        Args:
            param_name: The list of parameters to be removed.
            param_type: The type of new parameters to be removed.

        Raises:
            CustomExceptions.ParameterNotFoundError: If any of the parameter does not exist in the method.

        Returns:
            None.
        """

        for existing_param_name, _ in self._params:
            if existing_param_name == param_name:
                self._params.remove((existing_param_name, _))
                return
        raise CustomExceptions.ParameterNotFoundError(param_name)

    def change_parameters(self, op_name: str, old_type: type, np_name: str, new_type: type):
        """
        Changes a parameter in the method by replacing an old parameter with a new parameter.

    Args:
        op_name (str): The name of the parameter to be replaced.
        old_type (type): The type of the parameter to be replaced.
        np_name (str): The name of the new parameter to be added.
        new_type (type): The type of the new parameter to be added.

    Raises:
        CustomExceptions.ParameterNotFoundError: If the old parameter does not exist in the method.
        CustomExceptions.ParameterExistsError: If a parameter with the new name already exists in the method.

    Returns:
        None.
        """

        if any(param[0] == np_name for param in self._params):
            raise CustomExceptions.FieldExistsError(np_name)

        param_found = False

        for index, (param_name, param_type) in enumerate(self._params):
            if param_name == op_name and param_type == old_type:
                self._params[index] = (np_name, new_type)
                param_found = True
                break

        if not param_found:
            raise CustomExceptions.FieldNotFoundError(op_name)

    def __str__(self):
        """

        Returns the name of the method and a list of it's parameters.

        Args:
            None.

        Raises:
            None.

        Returns:
            name (str): A templated string to represent a method and
                its list of parameters.
        """

        result = f"\n{self.get_method_name()}"
        result_return_type = 'void' if self._return_type is type(None) else self._return_type
        result += f"\n\tReturn Type: {result_return_type}"
        result += "\n\t" + self.get_method_name() + "'s Params: "
        param_results = ' '.join(f'{name}: {ptype if ptype else " "}' for name, ptype in self._params)
        return result + param_results

    def __eq__(self, other):

        """ Equality operator for Methods - checks equality of both fields"""

        if not isinstance(other, UML_Method):
            return False

            # Compare the method names
        if self._name != other._name:
            return False

            # Compare the lengths of the parameters list
        if len(self._params) != len(other._params):
            return False

            # Compare each parameter
        for param in self._params:
            if param not in other._params:
                return False

        return True
