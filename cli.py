import logging
from parser import FixedWidthFile
from models import Transaction

logging.basicConfig(
    filename='cli.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

class CLI:
    def __init__(self, filepath):
        self.file = FixedWidthFile(filepath)
        self.file.read()

    def run(self):
        print("Welcome to FixedWidth CLI!")
        print("Available commands: get, change, add, save, exit")

        while True:
            command = input("Command: ").strip().lower()

            if command == "get":
                self.get_field()
            elif command == "change":
                self.change_field()
            elif command == "add":
                self.add_transaction()
            elif command == "save":
                self.save_file()
            elif command == "exit":
                logging.info("CLI session ended.")
                print("Goodbye!")
                break
            else:
                print("Invalid command! Available: get, change, add, save, exit")

    def get_field(self):
        obj, attr = self._input_field()
        try:
            value = getattr(obj, attr)
            print(f"Value: {value}")
            logging.info(f"Got {attr} value: {value}")
        except AttributeError:
            print("Field not found.")
            logging.error(f"Attempted to get invalid field '{attr}'.")

    def change_field(self):
        obj, attr = self._input_field()
        new_value = input("Enter new value: ").strip()
        try:
            if hasattr(obj, attr):
                setattr(obj, attr, new_value)
                logging.info(f"Changed {attr} to {new_value}")
                print(f"Updated {attr}.")
            else:
                print("Field not found.")
                logging.error(f"Attempted to change invalid field '{attr}'.")
        except Exception as e:
            logging.error(f"Error changing field: {e}")

    def add_transaction(self):
        try:
            amount = float(input("Enter amount (e.g., 100.00): "))
            currency = input("Enter currency (USD, EUR, PLN): ").strip().upper()
            counter = len(self.file.transactions) + 1
            new_trans = Transaction(counter=counter, amount=amount, currency=currency)
            self.file.transactions.append(new_trans)
            logging.info(f"Added transaction #{counter}: {amount} {currency}")
            print(f"Transaction #{counter} added.")
        except ValueError:
            print("Invalid amount. Transaction not added.")
            logging.error("Failed to add transaction due to invalid amount.")

    def save_file(self):
        try:
            self.file.write()
            logging.info("File saved successfully.")
            print("File saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
            print(f"Failed to save file: {e}")

    def _input_field(self):
        section = input("Choose section (header/footer): ").strip().lower()
        attr = input("Enter field name (e.g., name, surname, total_counter): ").strip()

        if section == "header":
            return self.file.header, attr
        elif section == "footer":
            return self.file.footer, attr
        else:
            print("Invalid section. Defaulting to header.")
            return self.file.header, attr


if __name__ == "__main__":
    cli = CLI("data.txt")
    cli.run()
