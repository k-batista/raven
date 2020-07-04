
from typing import List

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from rule_engine import Rule
# https://github.com/zeroSteiner/rule-engine


@dataclass_json
@dataclass
class SetupDataclass:
    name: str
    rule: Rule

    def matches(self, value):
        return self.rule.matches(value)

    def get_name(self):
        return self.name


@dataclass_json
@dataclass
class SetupFactory:
    setups: List[SetupDataclass] = field(default_factory=list)

    def add(self, name, expression):
        self.setups.append(SetupDataclass(name, Rule(expression)))

    def get_setups(self):
        return self.setups

    def find_setup(self, stocks):
        if stocks:
            for rule in self.get_setups():
                match = rule.matches(stocks)
                if match:
                    return rule.get_name()

        return None
