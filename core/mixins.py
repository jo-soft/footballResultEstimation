from numbers import Number


class ToVectorMixin:
    def to_vector(self, exclude_fields=[], keys=[]):
        if not keys:
            keys = self.keys
        return [
            getattr(self, key) for key in keys
            if (
                key not in exclude_fields
                ) and
                (
                isinstance(getattr(self, key), Number)
                )
            ]
