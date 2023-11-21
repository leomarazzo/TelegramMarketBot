from dataclasses import dataclass
from typing import List
from prettytable import PrettyTable, ALL
from textwrap import fill

@dataclass
class Item:
    name: str
    ammount: int
    price: float

    @property
    def total(self,):
        return self.ammount * self.price
    
    def serialize(self, list_number: int):
        return [fill(str(list_number), width=2),
                fill(self.name, width=11),
                fill(str(self.ammount), width=3),
                fill(str(self.total), width=9)]
    
    def serialize_detailed(self, list_number: int):
        return [str(list_number),
                self.name,
                str(self.ammount),
                str(self.price),
                str(self.total)]
    
    def serialize_csv(self,):
        return f"{self.name},{self.ammount},{self.price},{self.total}"


@dataclass
class MarketList:
    id: str
    items: List[Item]


    def add_item(self, message: str):
        product, ammount, price = message.rsplit(" ", 2)
        self.items.append(Item(
            name=product,
            ammount=int(ammount),
            price=float(price.replace(",", "."))
        ))

    def total(self,):
        total = sum(item.total for item in self.items)

        return total
    
    def get_total_row(self, table_str):
        last_row = table_str.split("\n")[0]
        row_length = len(last_row)
        total = str(self.total())
        total_col = f" {total} |"
        padding = " " * ((row_length - len(total_col) - 6) // 2)

        return f"|{padding}Total{padding}{total_col}\n{last_row}"

    
    def serialize(self,):
        table = PrettyTable(hrules=ALL)
        table.field_names = ['#', 'Product', 'Unit', 'Total']

        for i in range(len(self.items)):
            table.add_row(self.items[i].serialize(i+1))

        table_str = table.get_string() + "\n" + self.get_total_row(table.get_string())

        return '```\n{}```'.format(table_str)

    def serialize_detailed(self,):
        table = PrettyTable(hrules=ALL)
        table.field_names = ['#', 'Product', 'Unit', "Unit price", 'Total']

        for i in range(len(self.items)):
            table.add_row(self.items[i].serialize_detailed(i+1))

        table_str = table.get_string() + "\n" + self.get_total_row(table.get_string())

        return '```\n{}```'.format(table_str)
    
    def export(self, filename: str):
        with open(filename, 'w') as f:
            f.write("Product,Units,Unit Price,Total\n")
            for item in self.items:
                f.write(item.serialize_csv() + "\n")