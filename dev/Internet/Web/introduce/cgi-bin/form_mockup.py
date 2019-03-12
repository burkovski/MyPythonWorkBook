"""
Инструменты имитации результатов, возвращаемых конструктором cgi.
FieldStorage(); удобно для тестирования сценариев CGI из командной строки
"""


class FieldMockup:      # Имитируемый объект с входными даными
    def __init__(self, any_str):
        self.value = any_str


def form_mockup(**kwargs):          # Приеимает аргументы в виде поле=значение
    mockup = {}                     # Множественный выбор: [value, ...]
    for key, value in kwargs.items():
        if not isinstance(value, (list, tuple)):     # Простые поля, имеют атрибут .value
            mockup[key] = FieldMockup(str(value))
        else:                                        # Поля множественного выбора, являются списками
            mockup[key] = [FieldMockup(str(pick)) for pick in value]    # Добавить поля выгрузки
    return mockup


if __name__ == "__main__":
    def self_test():
        # Использовать эту форму, если поля определены жестко
        form = form_mockup(
            name="Bob",
            job="Hacker",
            food=("spam", "eggs", "ham")
        )
        print(form["name"].value)
        print(form["job"].value)
        for item in form["food"]:
            print(item.value, end=' ')
        print()
        # Использовать для имитации переменный из cgi.FieldStorage,
        # значения которых вычисляются динамически
        form = {
            "name": FieldMockup("Brian"),
            "age" : FieldMockup(42)
        }
        for key in form.keys():
            print(form[key].value)

    self_test()



