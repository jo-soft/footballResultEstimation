from collections import Callable


class Goal(object):

    def __init__(self, minute):
        self.minute = minute


class MatchData(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class NormalizedGameDataCollection(set):

    class NormalizedMatchData(MatchData):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

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
            return NormalizedGameDataCollection.NormalizedMatchData(**normalized_values)

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
