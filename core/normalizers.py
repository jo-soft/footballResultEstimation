class BasicNormalizer(object):

    def __init__(self, num_game_parts=8):
        """
        :param num_game_parts: default value of 8 leads to parts of 15 minutes incl. overtime
        """
        self.num_game_parts = num_game_parts
        self._gen_dict()

    def _gen_dict(self):
        self.fields_dict = {
            'team1': {
                'fn': self._team_name,
                'field': 'team1'
            },
            'team2': {
                'fn': self._team_name,
                'field': 'team2'
            },
            'goals_team1': lambda src, val: len(val),
            'goals_team2': lambda src, val: len(val),

            'max_goals_scored_team1': {
                'fn': self._max_goals_scored,
                'field': 'goals_team1'
            },
            'max_goals_scored_team2': {
                'fn': self._max_goals_scored,
                'field': 'goals_team2'
            },
            'match_goals_scored_team1': {
                'fn': self._match_goals_scored,
                'field': 'goals_team1'
            },
            'match_goals_scored_team2': {
                'fn': self._match_goals_scored,
                'field': 'goals_team2'
            },
            'match_goals_per_attempt_team1': {
                'fn': self._goals_per_attempt_team1,
                # field needs to be present be present
                # for compatibility reasons
                'field': 'goals_team1'
            },
            'match_goals_per_attempt_team2': {
                'fn': self._goals_per_attempt_team2,
                # field needs to be present be present
                # for compatibility reasons
                'field': 'goals_team2'  #
            },

            'max_attempts_team1': {
                'fn': self._max_attempts,
                'field': 'attempts_team1'
            },
            'max_attempts_team2': {
                'fn': self._max_attempts,
                'field': 'attempts_team2'
            },
            'match_attempts_team1': {
                'fn': self._match_attempts,
                'field': 'attempts_team1'
            },
            'match_attempts_team2': {
                'fn': self._match_attempts,
                'field': 'attempts_team2'
            },
            'max_attempts_on_target_team1': {
                'fn': self._max_attempts_on_target,
                'field': 'attempts_on_target_team1'
            },
            'max_attempts_on_target_team2': {
                'fn': self._max_attempts_on_target,
                'field': 'attempts_on_target_team2'
            },
            'match_attempts_on_target_team1': {
                'fn': self._match_attempts_on_target,
                'field': 'attempts_on_target_team1'
            },
            'match_attempts_on_target_team2': {
                'fn': self._match_attempts_on_target,
                'field': 'attempts_on_target_team2'
            },

            'max_corners_team1': {
                'fn': self._max_corners,
                'field': 'corners_team1'
            },
            'max_corners_team2': {
                'fn': self._max_corners,
                'field': 'corners_team2'
            },
            'match_corners_team1': {
                'fn': self._match_corners,
                'field': 'corners_team1'
            },
            'match_corners_team2': {
                'fn': self._match_corners,
                'field': 'corners_team2'
            },
            'max_offside_team1': {
                'fn': self._max_offside,
                'field': 'offside_team1'
            },
            'max_offside_team2': {
                'fn': self._max_offside,
                'field': 'offside_team2'
            },
            'match_offside_team1': {
                'fn': self._match_offside,
                'field': 'offside_team1'
            },
            'match_offside_team2': {
                'fn': self._match_offside,
                'field': 'offside_team2'
            },

            'max_fouls_committed_team1': {
                'fn': self._max_fouls_committed,
                'field': 'fouls_committed_team1'
            },
            'max_fouls_committed_team2': {
                'fn': self._max_fouls_committed,
                'field': 'fouls_committed_team2'
            },

            'match_fouls_committed_team1': {
                'fn': self._match_fouls_committed,
                'field': 'fouls_committed_team1'
            },
            'match_fouls_committed_team2': {
                'fn': self._match_fouls_committed,
                'field': 'fouls_committed_team2'
            },

            'max_fouls_suffered_team1': {
                'fn': self._max_fouls_suffered,
                'field': 'fouls_suffered_team1'
            },
            'max_fouls_suffered_team2': {
                'fn': self._max_fouls_suffered,
                'field': 'fouls_suffered_team2'
            },

            'match_fouls_suffered_team1': {
                'fn': self._match_fouls_suffered,
                'field': 'fouls_suffered_team1'
            },
            'match_fouls_suffered_team2': {
                'fn': self._match_fouls_suffered,
                'field': 'fouls_suffered_team2'
            }


        }

        for team in ('team1', 'team2'):
            for part in range(self.num_game_parts):
                match_goals_per_part = "match_goals_per_part_{}_of_{}_{}".format(
                    # add -1 in there because parts are numbered 0..num_game_parts - 1
                    part, self.num_game_parts - 1, team
                )

                def create_match_goals_per_part_fn(_team, _part):
                    return lambda src, val, obj, team=_team, part=_part, : self._goals_per_part(
                        team,
                        num_parts=self.num_game_parts,
                        part=part,
                        obj=obj
                )

                match_goals_per_part_dict = {
                    'fn': create_match_goals_per_part_fn(team, part),
                    # field needs to be present be present
                    # for compatibility reasons
                    'field': 'goals_{}'.format(team)
                }
                self.fields_dict[match_goals_per_part] = match_goals_per_part_dict

    def items(self):
        return self.fields_dict.items()

    def _max_data_fn(self, item, *args):
        return item/max(args)

    def _match_data_fn(self, item, *args):
        sum_items = sum(args)
        if sum_items == 0:
            return 0.5
        return item / sum_items

    def _max_asterisk(self, field1, field2,
                      src, val, obj=None,
                      mapping_fn=lambda x:x):
        max_val_team1 = 0
        max_val_team2 = 0
        for item in src.raw_data_iterator():
            match_val_team1 = mapping_fn(getattr(item, field1))
            if match_val_team1 > max_val_team1:
                max_val_team1 = match_val_team1
            match_val_team2 = mapping_fn(getattr(item, field2))
            if match_val_team2 > max_val_team2:
                max_val_team2 = match_val_team2
        return self._max_data_fn(mapping_fn(val), max_val_team1, max_val_team2)

    def _match_asterisk(self, field1, field2,
                        src, val, obj=None,
                        mapping_fn=lambda x:x):
        match_val_team1 = mapping_fn(
            getattr(obj, field1)
        )
        match_val_team2 = mapping_fn(
            getattr(obj, field2)
        )
        return self._match_data_fn(mapping_fn(val),
                                   match_val_team1,
                                   match_val_team2)

    def _max_goals_scored(self, src, val, obj):
        return self._max_asterisk(
            'goals_team1', 'goals_team2', src, val, obj, len
        )

    def _match_goals_scored(self, src, val, obj):
        return self._match_asterisk(
            'goals_team1', 'goals_team2', src, val, obj, len
        )

    def _max_attempts(self, src, val, obj):
        return self._max_asterisk(
            'attempts_team1', 'attempts_team2', src, val, obj
        )

    def _match_attempts(self, src, val, obj):
        return self._match_asterisk(
            'attempts_team1', 'attempts_team2', src, val, obj
        )

    def _max_attempts_on_target(self, src, val, obj):
        return self._max_asterisk(
            'attempts_on_target_team1', 'attempts_on_target_team2', src, val, obj
        )

    def _match_attempts_on_target(self, src, val, obj):
        return self._match_asterisk(
            'attempts_on_target_team1', 'attempts_on_target_team2', src, val, obj
        )

    def _max_corners(self, src, val, obj):
        return self._max_asterisk(
            'corners_team1', 'corners_team2', src, val, obj
        )

    def _match_corners(self, src, val, obj):
        return self._match_asterisk(
            'corners_team1', 'corners_team2', src, val, obj
        )

    def _max_offside(self, src, val, obj):
        return self._max_asterisk(
            'offside_team1', 'offside_team2', src, val, obj
        )

    def _match_offside(self, src, val, obj):
        return self._match_asterisk(
            'offside_team1', 'offside_team2', src, val, obj
        )

    def _max_fouls_committed(self, src, val, obj):
        return self._max_asterisk(
            'fouls_committed_team1', 'fouls_committed_team2', src, val, obj
        )

    def _match_fouls_committed(self, src, val, obj):
        return self._match_asterisk(
            'fouls_committed_team1', 'fouls_committed_team2', src, val, obj
        )

    def _max_fouls_suffered(self, src, val, obj):
        return self._max_asterisk(
            'fouls_suffered_team1', 'fouls_suffered_team2', src, val, obj
        )

    def _match_fouls_suffered(self, src, val, obj):
        return self._match_asterisk(
            'fouls_suffered_team1', 'fouls_suffered_team2', src, val, obj
        )

    def _team_name(self, src, val, obj=None):
        return val.lower()

    def _goals_per_attempt(self, team, obj):
        attempts_field_name = 'attempts_{}'.format(team)
        goals_field_name = 'goals_{}'.format(team)

        attempts = getattr(obj, attempts_field_name)
        goals = getattr(obj, goals_field_name)

        return len(goals) / attempts

    def _goals_per_attempt_team1(self, src, val, obj=None):
        return self._goals_per_attempt('team1', obj)

    def _goals_per_attempt_team2(self, src, val, obj=None):
        return self._goals_per_attempt('team2', obj)

    def _goals_per_part(self, team, num_parts, part, obj):

        def goal_to_minute(goal):
            # handle overtime
            minute_str = goal.minute.split('+')[0]

            return int(minute_str)

        goals_field_name = 'goals_{}'.format(team)
        goals = [goal_minute for goal_minute in map(
            goal_to_minute,
            getattr(obj, goals_field_name)
            )]

        part_length = 120 / num_parts
        part_start = part * part_length
        part_end = (part + 1) * part_length

        return len(
            [
                goal for goal in goals if
                part_start < goal <= part_end
            ]
        )
