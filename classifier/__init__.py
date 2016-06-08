from core.gameData import NormalizedMatchData
from core.teamSelector import TeamSelector


class TrainingItem(object):

    def __init__(self, vector, result):
        self.vector = vector
        self.result = result


def generate_training_data(dataset, team):
    ts = TeamSelector(dataset, team)

    exclude_fields = [
        'team_goals',
        'opponent_goals'
    ]
    return [
        TrainingItem(
            NormalizedMatchData(**item).to_vector(exclude_fields=exclude_fields),
            (item['team_goals'], item['opponent_goals'])
        )
        for item in ts.items()
    ]
