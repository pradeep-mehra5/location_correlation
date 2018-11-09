from auxiliary_fns import getDistance
from reverse_geocoding import createLocationDictionary
import datetime
import global_vars

UNCLASSIFIED = False
NOISE = None
CLUSTER_LIST = []

CLUSTER_DICT = {}


def _eps_neighborhood(p, q, eps):
    return getDistance(p[1],p[0],q[1],q[0])<eps;

def _region_query(m, point_id, eps):
    n_points = len(m[0])
    seeds = []
    for i in range(0, n_points):
        if _eps_neighborhood(list([m[0][point_id],m[1][point_id]]) , list([m[0][i],m[1][i]]) , eps):
            seeds.append(i)
    return seeds


def _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    seeds = _region_query(m, point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        CLUSTER_DICT[cluster_id] = set({})
        for seed_id in seeds:
            classifications[seed_id] = cluster_id
            CLUSTER_DICT[cluster_id].add((m[0][seed_id],m[1][seed_id]))
        while len(seeds) > 0:
            current_point = seeds[0]
            results = _region_query(m, current_point, eps)
            if len(results) >= min_points:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or \
                            classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True


#   dbscan algorithm
def dbscan(m, eps, min_points):
    print(f'\n\nTime: {datetime.datetime.now()}\nClustering has started')
    cluster_id = 1
    n_points = len(m[1])
    classifications = [UNCLASSIFIED] * n_points
    for point_id in range(0, n_points):
        point = [m[0][point_id],m[1][point_id]]
        if classifications[point_id] == UNCLASSIFIED:
            if _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    CLUSTER_LIST = classifications
    print(f'\n\nTime: {datetime.datetime.now()}\nList of clusters is: \n{CLUSTER_LIST}')
    print(f'\n\nTime: {datetime.datetime.now()}\nCluster dictionary is:\n{CLUSTER_DICT}')

    global_vars.CLUSTER_LIST = CLUSTER_LIST
    global_vars.CLUSTER_DICT = CLUSTER_DICT
    createLocationDictionary()


def main():
    m = [[39.90073069733655,39.899079855491344,39.9008860769231,39.978848289855065 ,39.981109225 ,39.98103225000002, 39.97863413513517 ,39.98140922093023, 40.0023006763285 ],[116.38687045278456,116.37943961849712,116.38650571428569,116.32662847826084, 116.30907245 ,116.31030393478255, 116.32625096396397 ,116.31101056976746 ,116.17073342028988 ]]
    eps = 200
    min_points = 2
    dbscan(m, eps, min_points)
    print(CLUSTER_DICT)

if __name__ == '__main__':
    main()