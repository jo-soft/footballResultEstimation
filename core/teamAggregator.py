from core.gameData import NormalizedMatchData


class AbstractAggregator(object):

    def __init__(self, data, value_fn,
                 team_field_name="team", opponent_field_name="opponent", exclude_fields=[]):
        self.value_fn = value_fn
        self.data = data
        self.exclude_fields = [team_field_name, opponent_field_name, 'date']
        self.exclude_fields.extend(exclude_fields)

    def filter(self, items):
        return items

    def items(self):
        keys = None
        for item in self.data.items():
            if not keys:
                keys = item.keys()
                tmp_dict = {
                    key: [] for key in keys
                }
            if not keys == item.keys():
                raise ValueError("incompatible fields")
            for key, value in item.items():
                tmp_dict[key].append(value)
        data = {
            key: self.value_fn(
                self.filter(value)
            ) for key, value in tmp_dict.items()
            if key not in self.exclude_fields
        }
        return NormalizedMatchData(**data)


class ExcludeUpperValPercentageFilterMixin:
    """
    excludes all values bigger than ``self.threshold``  * max val
    """
    def filter(self, items):
        max_val = max(items)
        return (
            item for item in items
            if item <= (1 - self.threshold) * max_val
        )


class ExcludeUpperCountPercentageFilterMixin:
    """
    excludes the upper ``self.threshold`` size items
    """
    def filter(self, items):
        items.sort()
        count = (1 - self.threshold) * len(items)
        return items[:int(count)]


class AvgAggregator(AbstractAggregator):

    def __init__(self, data, *args, **kwargs):
        from statistics import mean
        super(AvgAggregator, self).__init__(data, mean, *args, **kwargs)


class AvgFilteredValAggregator(AvgAggregator, ExcludeUpperValPercentageFilterMixin):
    def __init__(self, data, threshold, *args, **kwargs):
        super(AvgFilteredValAggregator, self).__init__(data, *args, **kwargs)
        self.threshold = threshold


class AvgFilteredCountAggregator(AvgAggregator, ExcludeUpperCountPercentageFilterMixin):
    def __init__(self, data, threshold, *args, **kwargs):
        super(AvgFilteredCountAggregator, self).__init__(data, *args, **kwargs)
        self.threshold = threshold


class MaxAggregator(AbstractAggregator):
    def __init__(self, data, *args, **kwargs):
        super(MaxAggregator, self).__init__(data, max, *args, **kwargs)


class FilteredValMaxAggregator(MaxAggregator, ExcludeUpperValPercentageFilterMixin):
    def __init__(self, data, threshold, *args, **kwargs):
        super(FilteredValMaxAggregator, self).__init__(data, *args, **kwargs)
        self.threshold = threshold


class FilteredCountMaxAggregator(MaxAggregator, ExcludeUpperCountPercentageFilterMixin):
    def __init__(self, data, threshold, *args, **kwargs):
        super(FilteredCountMaxAggregator, self).__init__(data, *args, **kwargs)
        self.threshold = threshold
