from __future__ import annotations

from functools import wraps
from typing import Callable, Dict, List, Tuple


WELCOME_MESSAGE = "Welcome to the assistant bot!"
GOODBYE_MESSAGE = "Good bye!"
HELLO_MESSAGE = "How can I help you?"
INVALID_COMMAND_MESSAGE = "Invalid command."
CONTACT_NOT_FOUND_MESSAGE = "Contact not found."
NO_CONTACTS_MESSAGE = "No contacts saved."


def input_error(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return CONTACT_NOT_FOUND_MESSAGE
        except (ValueError, IndexError):
            if func.__name__ in {"add_contact", "change_contact"}:
                return "Give me name and phone please."
            if func.__name__ == "show_phone":
                return "Enter user name."
            return INVALID_COMMAND_MESSAGE

    return inner


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []

    command, *args = parts
    return command.lower(), args


@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    name, phone = args
    current_phone = contacts[name]
    if current_phone == phone:
        return "Contact updated."
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    name = args[0]
    return contacts[name]


@input_error
def show_all(args: List[str], contacts: Dict[str, str]) -> str:
    if args:
        raise ValueError

    if not contacts:
        return NO_CONTACTS_MESSAGE

    return "\n".join(
        f"{name}: {phone}" for name, phone in sorted(contacts.items())
    )


@input_error
def say_hello(args: List[str]) -> str:
    if args:
        raise ValueError
    return HELLO_MESSAGE


@input_error
def say_goodbye(args: List[str]) -> str:
    if args:
        raise ValueError
    return GOODBYE_MESSAGE


def handle_command(command: str, args: List[str], contacts: Dict[str, str]) -> str:
    if command == "hello":
        return say_hello(args)
    if command == "add":
        return add_contact(args, contacts)
    if command == "change":
        return change_contact(args, contacts)
    if command == "phone":
        return show_phone(args, contacts)
    if command == "all":
        return show_all(args, contacts)
    if command in {"close", "exit"}:
        return say_goodbye(args)
    return INVALID_COMMAND_MESSAGE


def main() -> None:
    contacts: Dict[str, str] = {}
    print(WELCOME_MESSAGE)

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        response = handle_command(command, args, contacts)
        print(response)

        if command in {"close", "exit"} and response == GOODBYE_MESSAGE:
            break


if __name__ == "__main__":
    main()
