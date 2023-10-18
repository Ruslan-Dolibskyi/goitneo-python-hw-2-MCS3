def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"Unexpected error: {e}"

    return inner

@input_error
def hello(*args, contacts):
    return "How can I help you?"

@input_error
def add(*args, contacts):
    if len(args) < 2:
        raise ValueError
    username = args[0]
    phone = args[1]
    contacts[username] = phone
    return f"Added {username} with phone number {phone}"

@input_error
def change(*args, contacts):
    if len(args) < 2:
        raise ValueError
    username = args[0]
    phone = args[1]
    if username in contacts:
        contacts[username] = phone
        return f"Changed {username}'s phone number to {phone}"
    raise KeyError

@input_error
def phone(*args, contacts):
    if len(args) == 0:
        raise ValueError
    username = args[0]
    if username in contacts:
        return contacts[username]
    raise KeyError

@input_error
def all_contacts(*args, contacts):
    if not contacts:
        return "No contacts saved"
    return "\n".join([f"{username}: {number}" for username, number in contacts.items()])

@input_error
def exit_bot(*args, contacts):
    return "Good bye!"

@input_error
def unknown_command(*args, contacts):
    return "Unknown command. Try again"

COMMANDS = {
    hello: "hello",
    add: "add",
    change: "change",
    phone: "phone",
    all_contacts: "all",
    exit_bot: ("exit", "close")
}

def pars_command(line: str) -> tuple[callable, list]:
    for cmd, kwords in COMMANDS.items():
        if line.lower().startswith(kwords):
            return cmd, line.split(" ")[1:]
    return unknown_command, []

def main():
    contacts = {}
    while True:
        user_input = input("Enter command: ").strip()

        command, data = pars_command(user_input)
        print(command(*data, contacts=contacts))
    
        if command == exit_bot:
            break

if __name__ == "__main__":
    main()
