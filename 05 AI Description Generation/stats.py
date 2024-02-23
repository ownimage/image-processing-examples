import copy


class Stats:
    __stats = None
    EMPTY_STATS = {
        'count': 0, 'time': 0, 'time2': 0, 'first_time': 0, 'words': 0, 'words2': 0
    }

    def __init__(self):
        self.__stats = {}

    def get(self):
        return copy.deepcopy(self.__stats)

    def __get_stats(self, id):
        if id not in self.__stats:
            stats = copy.deepcopy(self.EMPTY_STATS)
            self.__stats[id] = stats
        return self.__stats[id]

    def add(self, id, time, words):
        stats = self.__get_stats(id)
        if stats['count'] == 0:
            stats['first_time'] = time
        else:
            stats['time'] += time
            stats['time2'] += time * time
        stats['words'] += words
        stats['words2'] += words * words
        stats['count'] += 1
