class BasicNormalizers(object):

    def items(self):
        normalise_dict = {
            'team1': {
                'fn': self._team_name,
                'field': 'team1'
            },
            'team2': {
                'fn': self._team_name,
                'field': 'team2'
            },


            'goals_scored_team1': {
                'fn': self._goals_scored,
                'field': 'goals_team1'
            },

            'goals_scored_team2': {
                'fn': self._goals_scored,
                'field': 'goals_team2'
            }
        }
        return normalise_dict.items()

    def _team_name(self, src, val):
        return val.lower()

    def _goals_scored(self, src, val):
        max_goals = max(
            max(
                len(getattr(item, 'goals_team1')),
                len(getattr(item, 'goals_team2'))
            ) for item in src.raw_data_iterator()
        )

        return len(val) / max_goals
