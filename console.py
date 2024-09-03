#!/usr/bin/env python3
"""
The console module.

Contains the entry point of the command interpreter.
"""
import cmd
import shlex

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class.

    Implements the command interpreter of the AirBNB project.
    """

    prompt = "(hbnb) "
    classes_list = [
        'BaseModel', 'User', 'State',
        'City', 'Amenity', 'Place', 'Review'
    ]

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, line):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file),
        and prints the id.
        """
        classes_dict = {
            'BaseModel': BaseModel, 'User': User,
            'State': State, 'City': City,
            'Amenity': Amenity,
            'Place': Place, 'Review': Review
        }

        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes_dict:
            new_dict = self._key_value_parser(args[1:])
            instance = classes_dict[args[0]](**new_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(instance.id)
        instance.save()

    def help_create(self):
        """Prints the help documentation for create."""
        print(
            """
            [Usage]: create <class name>

            Creates a new instance of BaseModel, saves it (to the JSON file),
            and prints the id.

            If the class name is missing, print ** class name missing **
            If the class name doesn't exist, print ** class doesn't exist **
            """
        )

    def do_show(self, line):
        """Shows Indvidual instance string representation."""
        if not line:
            print("** class name missing **")
            return

        instance_data = line.split(" ")

        # Check for instance id
        if len(instance_data) != 2:
            print("** instance id missing **")
            return

        # Check for instance name
        if instance_data[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        # Generate instance key from its name and id
        instance_key = "{}.{}".format(instance_data[0], instance_data[1])

        # Try print insatnce key if it exists
        try:
            print(storage._FileStorage__objects[instance_key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Prints the help documentation for show."""
        print(
            """
            [Usage]: show <class name> <id>

            Prints the string representation of an instance based on
            the class name and id.

            If the class name is missing, print ** class name missing **
            If the class name doesn't exist, print ** class doesn't exist **
            If the id is missing, print ** instance id missing **
            If the instance of the class name doesn't exist for the id,
            print ** no instance found **
            """
        )

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        if not line:
            print("** class name missing **")
            return

        instance_data = line.split(" ")

        # Check for instance id
        if len(instance_data) != 2:
            print("** instance id missing **")
            return

        # Check for instance name
        if instance_data[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        # Generate instance key from its name and id
        instance_key = "{}.{}".format(instance_data[0], instance_data[1])

        # Try delete insatnce key if it exists
        try:
            del(storage.all()[instance_key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Prints the help documentation for destroy."""
        print(
            """
            [Usage]: destroy <class name> <id>

            Deletes an instance based on the class name and id
            (save the change into the JSON file).

            If the class name is missing, print ** class name missing **
            If the class name doesn't exist, print ** class doesn't exist **
            If the id is missing, print ** instance id missing **
            If the instance of the class name doesn't exist for the id,
            print ** no instance found **
            """
        )

    def do_all(self, line):
        """
        Prints all string representation of all instances based
        or not on the class name.
        """
        print_list = []

        if line:
            args = line.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes_list:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """Prints the help documentation for all."""
        print(
            """
            [Usage]: all (<class name>)
            Brackets indicates optional args.

            The printed result is a list of strings.
            If the class name doesn't exist, print ** class doesn't exist **
            """
        )

    def do_update(self, line):
        """Updates an instance based on the class name and id."""

        args = shlex.split(line)

        # Check if args are empty
        if len(args) < 1:
            print("** class name missing **")
            return

        # Check if instance id is present
        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_data = args[:2]  # Class name > [0] and instance id > [1]

        # Now check if class name is valid
        if instance_data[0] not in HBNBCommand.classes_list:
            print("** class doesn't exist **")
            return

        # Genrate the key to check if instance exists
        instance_key = "{}.{}".format(instance_data[0], instance_data[1])
        if instance_key not in storage.all():
            print("** no instance found **")
            return

        # Check if attribute name is present
        if len(args) < 3:
            print("** attribute name missing **")
            return

        # Check if attribute value is present
        if len(args) < 4:
            print("** value missing **")
            return

        instance_attr_data = args[2:4]  # attribute name > [0] and value > [1]
        instance = storage.all()[instance_key]
        # Casting attribute value to the correct type
        if hasattr(instance, instance_attr_data[0]):
            attr_type = type(getattr(instance, instance_attr_data[0]))
            attribute_value = attr_type(instance_attr_data[1])

        setattr(instance, instance_attr_data[0], instance_attr_data[1])
        instance.save()

    def help_update(self):
        """Prints the help documentation for update."""
        print(
            """
            [Usage]: update <class name> <id> <attr name> "<attr value>"

            Updates an instance based on the class name and id by adding or
            updating attribute (save the change into the JSON file).

            If the class name is missing, print ** class name missing **
            If the class name doesn't exist, print ** class doesn't exist **
            If the id is missing, print ** instance id missing **
            If the instance of the class name doesn't exist for the id,
            print ** no instance found **
            If the attribute name is missing,
            print ** attribute name missing **
            If the value for the attribute name doesn't exist,
            print ** value missing **
            """
        )

    def do_EOF(self, line):
        """Exit the interpreter using the EOF Flag."""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF."""
        print(
            """
            [Usage]: ^D

            Exits the program without formatting
            """
        )

    def do_quit(self, line):
        """Exit the interpreter using the quit command."""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit."""
        print(
            """
            [Usage]: quit

            Exits the program with formatting
            """
        )

    def emptyline(self):
        """Do nothing on empty input line."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
