import jsonpickle
import importlib

from collections import Callable
from core.mixins import ToVectorMixin


class Goal(object):

    def __init__(self, minute):
        self.minute = minute


class MatchData(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class NormalizedMatchData(MatchData, ToVectorMixin):

    def __init__(self, **kwargs):
        super(NormalizedMatchData, self).__init__(**kwargs)
        self.keys = list(kwargs.keys())
        # ensure keys always have the same order
        self.keys.sort()


class NormalizedGameDataCollection(set):
    """
    known bug:
       normaliser constructor parameters get lost when using to_json/from_json.
    """
    @classmethod
    def from_json(cls, file_path):
        with open(file_path) as f:
            json_str = f.read()
        normalizer_class_module, normalizer_class_name, data = jsonpickle.decode(json_str)

        mod = importlib.import_module(normalizer_class_module)
        return cls(getattr(mod, normalizer_class_name)(), data)

    def to_json(self, file_path):
        with open(file_path, 'w') as f:
            json_data = jsonpickle.encode(
                (
                    self.normalizer.__class__.__module__,
                    self.normalizer.__class__.__name__,
                    [item for item in self.raw_data_iterator()]
                )
            )
            f.write(json_data)

    def teams(self):
        # it's enough to consider team1 here because every team is at
        # least once team1 (during the qualification phase)
        return set(
            item.team1 for item in self
        )

    class NormalizedIterator(object):

        def __init__(self, src):
            self.src = src
            self._iter = self.src.raw_data_iterator()

        def __next__(self):

            def get_normalize_fn(key, fn_or_dict):
                if isinstance(fn_or_dict, Callable):
                    return lambda _src, _val: fn_or_dict(_src, getattr(_val, key))

                field = fn_or_dict.get('field')
                fn = fn_or_dict.get('fn')
                if fn and field:
                    return lambda _src, _val: fn(_src, getattr(_val, field), _val)
                else:
                    raise ValueError()

            val = self._iter.__next__()

            normalized_values = {
                key: get_normalize_fn(key, normalize_fn_or_dict)(
                    self.src,
                    val
                )
                for key, normalize_fn_or_dict in self.src.normalizer.items()
                }
            return NormalizedMatchData(**normalized_values)

    def __init__(self, normalizer, data=None):
        """
        Collection based on set for normalized game data.

        The fields of a ``NormalizedMatchData`` Element are exactly the
        keys of the ``normalizer`` param, while their value is
        ``normalizer[key](self, match_value)`` where ``match_value``
        is the raw data field for key from associated MatchData object.
        :param normalizer: dict of normalising functions
        :param data: initial data
        """
        super(NormalizedGameDataCollection, self).__init__(data)
        self.normalizer = normalizer

    def __iter__(self):
        """
        :return: NormalizedIterator
        """
        return NormalizedGameDataCollection.NormalizedIterator(self)

    def raw_data_iterator(self):
        """
        Helper method to access the raw data
        this enables to access self.__next__
        :return:  self
        """
        return super(NormalizedGameDataCollection, self).__iter__()
