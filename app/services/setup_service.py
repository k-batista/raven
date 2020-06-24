
from app.config.app_context import ApplicationContext

from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from rule_engine import Rule
# https://github.com/zeroSteiner/rule-engine


@dataclass_json
@dataclass
class RuleTag:
    name: str
    rule: Rule

    def matches(self, value):
        return self.rule.matches(value)

    def get_name(self):
        return self.name


@dataclass_json
@dataclass
class Politic:
    rules: List[RuleTag] = field(default_factory=list)

    def add(self, name, expression):
        self.rules.append(RuleTag(name, Rule(expression)))

    def get_rules(self):
        return self.rules


def find_setup(ticker):
    app = ApplicationContext.instance()

    list_stock = app.stock_repository.find_all_stocks_by_ticker(ticker)

    if not list_stock or len(list_stock) == 0:
        return None

    stocks = dict()

    politic = Politic()
    politic.add('Possível Setup 9.1 de Compra',
                """ stock_0_price_close >= stock_0_ema_9
        and stock_1_price_close <= stock_0_ema_9
        and stock_2_price_close <= stock_0_ema_9
        """)
    politic.add('Possível Setup 9.2 de Compra',
                """ stock_0_price_close < stock_1_price_close
        and stock_0_price_close < stock_0_price_open
        and stock_0_price_close >= stock_0_ema_9
        and stock_0_ema_9 > stock_1_ema_9
        and stock_1_ema_9 > stock_2_ema_9
        and stock_2_ema_9 > stock_3_ema_9
        and stock_3_ema_9 > stock_4_ema_9
        and stock_4_ema_9 > stock_5_ema_9
        """)
    politic.add('Possível Setup 9.3 de Compra',
                """ stock_0_price_close < stock_2_price_close
        and stock_1_price_close < stock_2_price_close
        and stock_0_price_close >= stock_0_ema_9
        and stock_1_price_close >= stock_0_ema_9
        and stock_0_ema_9 > stock_1_ema_9
        and stock_1_ema_9 > stock_2_ema_9
        and stock_2_ema_9 > stock_3_ema_9
        and stock_3_ema_9 > stock_4_ema_9
        and stock_4_ema_9 > stock_5_ema_9
        """)

    politic.add('Possível PC de Compra',
            """ stock_0_price_low <= stock_0_ema_21
    and stock_0_price_close <= stock_1_price_close
    and stock_1_price_close <= stock_2_price_close
    and stock_2_price_close <= stock_3_price_close
    and stock_0_price_close >= stock_0_ema_21
    and stock_1_price_close >= stock_0_ema_21
    and stock_2_price_close >= stock_0_ema_21
    and stock_3_price_close >= stock_0_ema_21
    and stock_4_price_close >= stock_0_ema_21
    and stock_5_price_close >= stock_0_ema_21
    """)

    for key, value in enumerate(list_stock):
        stocks[f'stock_{key}_price_close'] = float(value.price_close)
        stocks[f'stock_{key}_price_open'] = float(value.price_open)
        stocks[f'stock_{key}_price_low'] = float(value.price_low)
        stocks[f'stock_{key}_date'] = value.des_date
        stocks[f'stock_{key}_ema_9'] = float(value.ema_9())
        stocks[f'stock_{key}_ema_21'] = float(value.ema_21())

    for rule in politic.get_rules():
        match = rule.matches(stocks)
        if match:
            return rule.get_name()

    return None
