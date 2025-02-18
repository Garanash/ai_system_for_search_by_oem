class Article:
    def __init__(self, name, OEM_number):
        self.name = name
        self.OEM_number = OEM_number


class Provider:
    end_price: str

    def __init__(self, label, country, broker, pay_by_broker, price, currency):
        self.label = label
        self.country = country
        self.broker = broker
        self.pay_by_broker = pay_by_broker
        self.price = price
        self.currency = currency

    def convert_price_from_currency(self):
        valuta = {"Euro": 95.5,
                  "USD": 91.33,
                  "CNY": 12.59,
                  "CAD": 64.36}
        try:
            try:
                self.price = int(self.price.strip())
            except:
                self.end_price = 10**60
            self.end_price = self.price * valuta[self.currency]
        except TypeError:
            self.end_price = "None"
        except KeyError:
            self.end_price = "None"
