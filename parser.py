from models import Header, Transaction, Footer
from utils import pad_right, format_amount, parse_amount
from constants import LINE_LENGTH

class FixedWidthFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.header = None
        self.transactions = []
        self.footer = None

    def read(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]

        self.header = Header(
            name=lines[0][2:30].strip(),
            surname=lines[0][30:60].strip(),
            patronymic=lines[0][60:90].strip(),
            address=lines[0][90:120].strip(),
        )

        self.transactions = [
            Transaction(
                counter=int(line[2:8]),
                amount=parse_amount(line[8:20]),
                currency=line[20:23].strip(),
                reserved=line[23:120].strip(),
            ) for line in lines[1:-1]
        ]

        self.footer = Footer(
            total_counter=int(lines[-1][2:8]),
            control_sum=parse_amount(lines[-1][8:20]),
            reserved=lines[-1][20:120].strip(),
        )

    def write(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            # header
            header_line = f"01{pad_right(self.header.name, 28)}{pad_right(self.header.surname, 30)}" \
                          f"{pad_right(self.header.patronymic, 30)}{pad_right(self.header.address, 30)}"
            f.write(header_line[:LINE_LENGTH] + '\n')

            # transactions
            for transaction in self.transactions:
                counter_str = f"{transaction.counter:06d}"
                amount_str = format_amount(transaction.amount)
                trans_line = f"02{counter_str}{amount_str}{pad_right(transaction.currency,3)}{pad_right(transaction.reserved,97)}"
                f.write(trans_line[:LINE_LENGTH] + '\n')

            # footer
            total_counter = len(self.transactions)
            control_sum = sum(t.amount for t in self.transactions)
            footer_line = f"03{total_counter:06d}{format_amount(control_sum)}{pad_right('',100)}"
            f.write(footer_line[:LINE_LENGTH] + '\n')
