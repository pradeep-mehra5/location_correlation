import numpy as np
from auxiliary_fns import getDistance

UNCLASSIFIED = False
NOISE = None


def _eps_neighborhood(p, q, eps):
    return getDistance(p[1],p[0],q[1],q[0])<eps;

def _region_query(m, point_id, eps):
    # n_points = m.shape[1]  #when using hardcoded numpy
    n_points = len(m[0])   #when used as a module
    seeds = []
    for i in range(0, n_points):
        # if _eps_neighborhood(m[:, point_id], m[:, i], eps):  #when using hardcoded numpy
        if _eps_neighborhood(list([m[0][point_id],m[1][point_id]]) , list([m[0][i],m[1][i]]) , eps): #when used as a module
            seeds.append(i)
    return seeds


def _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    seeds = _region_query(m, point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id

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


def dbscan(m, eps, min_points):
    cluster_id = 1
    # n_points = m.shape[1] #when using hardcoded numpy
    n_points = len(m[1])  #when used as a module
    classifications = [UNCLASSIFIED] * n_points
    for point_id in range(0, n_points):
        # point = m[:, point_id] #when using hardcoded numpy
        point = [m[0][point_id],m[1][point_id]]  #when used a module
        if classifications[point_id] == UNCLASSIFIED:
            if _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    return classifications

def main():
    m = np.matrix('39.978848289855065 39.981109225 39.98103225000002 39.97863413513517 39.98140922093023 40.0023006763285 ; 116.32662847826084 116.30907245 116.31030393478255 116.32625096396397 116.31101056976746 116.17073342028988 ')
    eps = 200
    min_points = 2
    print(dbscan(m, eps, min_points))

if __name__ == '__main__':
    main()