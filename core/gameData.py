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

    class NormalisedIterator(object):

        def __init__(self, src, normalisers):
            self.src = src
            self.normalisers = normalisers

        def __next__(self):
            val = self.src.__next__()

            normalised_values = {
                key: normalise_fn(
                    self.src,
                    getattr(val, key)
                )
                for key, normalise_fn in self.normalisers.items()
                }
            return NormalizedGameDataCollection.NormalizedMatchData(**normalised_values)

    def __init__(self, normalisers, data=None):
        super(NormalizedGameDataCollection, self).__init__(data)
        self.normalisers = normalisers

    def __iter__(self):
        """
        :return: NormalisedIterator
        """
        raw_data_iterator = self.raw_data_iterator()
        return NormalizedGameDataCollection.NormalisedIterator(raw_data_iterator, self.normalisers)

    def raw_data_iterator(self):
        """
        Helper method to access the raw data
        this enables to access self.__next__
        :return:  self
        """
        return super(NormalizedGameDataCollection, self).__iter__()
