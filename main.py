import datetime


class Item:
    def __init__(self, item, cardinality):
        self.item = item
        self.cardinality = cardinality

    def check_item_cardinality(self):
        if self.cardinality == 'one':
            return True
        elif self.cardinality == 'many':
            return False


class Person:
    def __init__(self, name, item, value, removable):
        self.name = name
        self.item = item
        self.value = value
        self.removable = removable
        self.addition_date = datetime.datetime.now()

    # if last item = True, keep the fact
    def check_fact(self):
        if self.removable:
            return self


def get_actual_facts(facts, schemas):
    # it will sort by first element (name)
    facts.sort()

    actual_facts = []
    # loop to decide which fact will be returned based on last parameter (boolean)
    for fact in facts:
        name, item, value, removable = fact
        person = Person(name, item, value, removable)
        person = person.check_fact()

        if person:
            actual_facts.append(fact)
            assert person.removable, 'This fact cannot be added to the final list'

    oldest_facts = []
    for schema in schemas:
        item, cardinality = schema
        schema = Item(item, cardinality)
        is_unique = schema.check_item_cardinality()

        # loop to decide which fact will be returned if item has cardinality = 'one'
        if is_unique:
            i = 0

            for fact in actual_facts:
                name, item, value, removable = fact
                actual_person = Person(name, item, value, removable)

                if i + 1 < len(actual_facts):
                    next_fact = actual_facts[i + 1]
                    name, item, value, removable = next_fact
                    next_person = Person(name, item, value, removable)

                    # since the list is sorted by name, if the next name is equal to the actual one,
                    # and the item is the same of actual schema's, select the oldest ones (by date) to exclude
                    if actual_person.item == schema.item and next_person.item == schema.item and actual_person.name == next_person.name:
                        if actual_person.addition_date < next_person.addition_date:
                            oldest_facts.append(fact)
                            assert len(oldest_facts), 'This fact will be included in final list'
                    i += 1

    # Updating actual_facts list
    for fact in facts:
        for old_fact in oldest_facts:
            if fact == old_fact:
                actual_facts.pop(actual_facts.index(old_fact))

    facts = actual_facts
    for fact in facts:
        print(facts.index(fact), fact)


def main():
    schemas = [
        ('endereco', 'one'),
        ('telefone', 'many')
    ]
    facts = [
        ('gabriel', 'endereco', 'av rio branco, 109', True),
        ('joao', 'endereco', 'rua alice, 10', True),
        ('joao', 'endereco', 'rua bob, 88', True),
        ('joao', 'telefone', '234-5678', True),
        ('joao', 'telefone', '91234-5555', True),
        ('joao', 'telefone', '234-5678', False),
        ('gabriel', 'telefone', '98888-1111', True),
        ('gabriel', 'telefone', '56789-1010', True),
    ]

    get_actual_facts(facts, schemas)


if __name__ == '__main__':
    main()
