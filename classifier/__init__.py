import itertools as it
from core.teamAggregator import AvgAggregator
from core.teamSelector import TeamSelector
from pybrain.datasets import SupervisedDataSet


class SupervisedMatchDataSet(SupervisedDataSet):

    def __init__(self, max_goals, *args, **kwargs):
        super(SupervisedMatchDataSet, self).__init__(*args, **kwargs)
        self.max_goals = max_goals


def generate_training_data(matches, aggregator_cls=AvgAggregator):
    exclude_fields = [
        'team_goals',
        'opponent_goals'
        'date'
    ]
    normalizer = matches.src.normalizer
    matches = [match for match in matches]
    matches.sort(key=lambda x: x.date)

    max_goals = max(it.chain(
        (match.goals_team1 for match in matches),
        (match.goals_team2 for match in matches)
    ))

    result = SupervisedMatchDataSet(max_goals,
                                    # exclude the un normalized goals
                                    2 * (len(matches[0].to_vector()) - 1),
                                    2)
    for pos, match in enumerate(matches):
        matches_before = matches[:pos+1]
        ts1 = TeamSelector(matches_before, match.team1, normalizer=normalizer)
        ts2 = TeamSelector(matches_before, match.team2, normalizer=normalizer)

        aggregated_values_team_1 = aggregator_cls(ts1).items()
        aggregated_values_team_2 = aggregator_cls(ts2).items()
        vector = tuple(
            it.chain.from_iterable(
                map(lambda x: x.to_vector(exclude_fields=exclude_fields),
                    (aggregated_values_team_1, aggregated_values_team_2)
                    )
            )
        )
        match_result = (match.max_goals_scored_team1, match.max_goals_scored_team2)
        result.addSample(vector, match_result)

    return result
