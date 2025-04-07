from dataclasses import dataclass

@dataclass
class Header:
    field_id: str = "01"
    name: str = ""
    surname: str = ""
    patronymic: str = ""
    address: str = ""

@dataclass
class Transaction:
    field_id: str = "02"
    counter: int = 0
    amount: float = 0.0
    currency: str = ""
    reserved: str = ""

@dataclass
class Footer:
    field_id: str = "03"
    total_counter: int = 0
    control_sum: float = 0.0
    reserved: str = ""
