
from __future__ import absolute_import, division, \
                       print_function, unicode_literals

import pytest

from crushlib.crushmap import CrushMap, Rule, Steps
from crushlib.crushmap.rules import StepTake, StepChoose, StepEmit


class TestRules(object):

    def test_rules_add(self, crushmap):
        r = Rule('test')
        crushmap.rules.add_rule(r)

        rf1 = Rule('fail', ruleset=-1)
        with pytest.raises(ValueError):
            crushmap.rules.add_rule(rf1)
        rf2 = Rule('fail', ruleset=0)
        with pytest.raises(IndexError):
            crushmap.rules.add_rule(rf2)
        rf3 = Rule('test')
        with pytest.raises(IndexError):
            crushmap.rules.add_rule(rf3)

    def test_rules_get(self, crushmap):

        r = crushmap.rules.get_rule(name='replicated_ruleset')
        assert isinstance(r, Rule)
        assert 0 == r.id

        r = crushmap.rules.get_rule(rule_id=0)
        assert isinstance(r, Rule)
        assert 'replicated_ruleset' == r.name

        with pytest.raises(ValueError):
            crushmap.rules.get_rule()
        with pytest.raises(ValueError):
            crushmap.rules.get_rule(rule_id=0, name='test')

        with pytest.raises(IndexError):
            crushmap.rules.get_rule(name='testABC')
        with pytest.raises(IndexError):
            crushmap.rules.get_rule(rule_id=71)

    def test_rule_init(self):
        Rule('test')

        with pytest.raises(ValueError):
            Rule('test', rule_type='test')

    def test_rule_default(self, crushmap):
        root_item = crushmap.get_item('root')
        host_type = crushmap.types.get_type('host')
        r = Rule.default(root_item, host_type)
        assert isinstance(r, Rule)
        assert 'replicated_ruleset' == r.name
        assert 'replicated' == r.type

    def test_steps_add(self, crushmap):
        """:type crushmap: CrushMap"""

        root = crushmap.get_item('root')
        host_type = crushmap.types.get_type('host')
        take = StepTake(item=root)
        choose = StepChoose(host_type)
        emit = StepEmit()

        steps = Steps()

        with pytest.raises(ValueError):
            steps.add_step(emit)
        with pytest.raises(ValueError):
            steps.add_step(choose)

        steps.add_step(take)
        steps.add_step(choose)

        with pytest.raises(ValueError):
            steps.add_step(take)

        steps.add_step(emit)

        with pytest.raises(ValueError):
            steps.add_step(emit)
        with pytest.raises(ValueError):
            steps.add_step(choose)

        steps.add_step(take)

        with pytest.raises(ValueError):
            Rule('test', steps=steps)

        steps.add_step(choose)
        steps.add_step(emit)
        Rule('test', steps=steps)

    def test_step_names(self, crushmap):
        item = crushmap.get_item('root')
        host = crushmap.types.get_type('host')

        assert StepTake(item).name == 'take'
        assert StepEmit().name == 'emit'
        assert StepChoose(host).name == 'choose'
        assert StepChoose(host, leaf=True).name == 'chooseleaf'
