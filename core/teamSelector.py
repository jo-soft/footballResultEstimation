class TeamSelector(object):

    def __init__(self, data, team):
        self.data = data
        self.team = team

    def items(self, team_only=False):
        normalizer = self.data.normalizer
        result = []
        for item in self.data:
            if item.team1 == self.team:
                team_pos = 1
            elif item.team2 == self.team:
                team_pos = 2
            else:
                # self.team is not part of the match
                continue
            team_str = "team{}".format(team_pos)

            def new_key_fn(key):
                if key.endswith(team_str):
                    result = "team_{}".format(key)
                elif team_only:
                    return None
                else:
                    result = "opponent_{}".format(key)
                return result[:-6]
            result.append(
                {
                    new_key_fn(key): getattr(item, key)
                    for key in normalizer.fields_dict.keys() if new_key_fn(key)
                }
            )
        return result