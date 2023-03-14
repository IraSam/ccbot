class CurrencyPair:
    def __init__(self, base: str, quote: str, base_precision: int, quote_precision: int):
        self.base = base
        self.quote = quote
        self.base_precision = base_precision
        self.quote_precision = quote_precision

    def __str__(self):
        return f'{self.base}/{self.quote}'

    @property
    def symbol(self):
        return f'{self.base}{self.quote}'
