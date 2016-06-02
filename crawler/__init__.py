class Goal(object):

    def __init__(self, minute):
        self.minute = minute


class MatchData(object):

    def __init__(self,
                 team1,
                 team2,
                 goals_team1,
                 goals_team2,
                 attempts_team1,
                 attempts_team2,
                 attempts_on_target_team1,
                 attempts_on_target_team2,
                 corners_team1,
                 corners_team2,
                 offside_team1,
                 offside_team2,
                 possession_team1,
                 possession_team2,
                 fouls_committed_team1,
                 fouls_committed_team2,
                 fouls_suffered_team1,
                 fouls_suffered_team2
                 ):
        self.team1 = team1
        self.team2 = team2
        self.goals_team1 = goals_team1
        self.goals_team2 = goals_team2
        self.attempts_team1 = attempts_team1
        self.attempts_team2 = attempts_team2
        self.attemptsOnTarget_team1 = attempts_on_target_team1
        self.attemptsOnTarget_team2 = attempts_on_target_team2
        self.corners_team1 = corners_team1
        self.corners_team2 = corners_team2
        self.offside_team1 = offside_team1
        self.offside_team2 = offside_team2
        self.possession_team1 = possession_team1
        self.possession_team2 = possession_team2
        self.fouls_committed_Team1 = fouls_committed_team1
        self.fouls_committed_Team2 = fouls_committed_team2
        self.fouls_suffered_Team1 = fouls_suffered_team1
        self.fouls_suffered_Team2 = fouls_suffered_team2
1