import numpy as np
import scipy.io
import scipy.sparse as sp


def read_movielens_mat_file():
    mat = scipy.io.loadmat("/Raw_Datasets/movielens_dataset.mat")
    H = mat['H'][0, 0]

    S = scipy.sparse.csr_matrix(H)
    nodes = np.arange(S.shape[0])
    hyperedges = []

    S_transpose = S.transpose().tolil()

    for i in range(S_transpose.shape[0]):
        hyperedges.append(np.sort(S_transpose.rows[i]))

    print("Total number of nodes - " + str(len(nodes)))
    print("Total number of hyperedges - " + str(len(hyperedges)))

    return nodes, hyperedges


def read_movielens_data_files():
    movie_ids = set([])

    hyperedges = []

    director_movieids = {}

    movieid_genreid = {}

    genreid_genrename = {}
    genrename_genreid = {}

    dataset_folder = "/home/darwin/workspace/HPRA/Raw_Datasets/movielens"

    movies_file_handle = open(dataset_folder + "/movies.dat", encoding="ISO-8859-1")
    next(movies_file_handle)
    for line in movies_file_handle.readlines():
        temp = line.split("\n")
        line_split = temp[0].split("\t")

        movie_ids.add(line_split[0])

    directors_file_handle = open(dataset_folder + "/movie_directors.dat", encoding="ISO-8859-1")
    next(directors_file_handle)
    for line in directors_file_handle.readlines():
        temp = line.split("\n")
        line_split = temp[0].split("\t")

        movieid = line_split[0]
        directorid = line_split[1]

        if directorid not in director_movieids:
            director_movieids[directorid] = []

        director_movieids[directorid].append(movieid)

    genre_file_handle = open(dataset_folder + "/movie_genres.dat", encoding="ISO-8859-1")
    next(genre_file_handle)
    for line in genre_file_handle.readlines():
        temp = line.split("\n")
        line_split = temp[0].split("\t")

        movieid = line_split[0]
        genre = line_split[1]

        if genre not in genrename_genreid:
            genreid = len(genrename_genreid)
            genrename_genreid[genre] = genreid
            genreid_genrename[genreid] = genre

        genreid = genrename_genreid[genre]

        if movieid not in movieid_genreid:
            movieid_genreid[movieid] = []

        movieid_genreid[movieid].append(genreid)

    for directorid in director_movieids:
        hyperedges.append(director_movieids[directorid])

    return movieid_genreid, genreid_genrename, movie_ids, hyperedges


def get_movielens_network(use_cc):

    movieid_genreid, genreid_genrename, movie_ids, hyperedges = read_movielens_data_files()

    nodes, hyperedges = validate_hyperedges(movieid_genreid.keys(), movie_ids, hyperedges)

    if use_cc == "True":
        nodes, hyperedges = get_largest_cc(nodes, hyperedges)

    print("Total number of nodes - " + str(len(nodes)))
    print("Total number of hyperedges - " + str(len(hyperedges)))

    movieid_genreid = dict((node, movieid_genreid[node]) for node in nodes)

    genreid_count = {}
    for movieid in movieid_genreid:
        genreids = movieid_genreid[movieid]
        for genreid in genreids:
            if genreid not in genreid_count:
                genreid_count[genreid] = 1
            else:
                genreid_count[genreid] += 1

    for genreid in genreid_count:
        print("class - " + str(genreid) + ", classname - " + str(genreid_genrename[genreid]) + ", count - " + str(genreid_count[genreid]))

    return list(nodes), hyperedges, movieid_genreid, genreid_genrename


#nodes, hyperedges = read_movielens_mat_file()
#print("Total number of nodes - " + str(len(nodes)))
#print("Total number of hyperedges - " + str(len(hyperedges)))

#print(len(nodes))
#print(len(hyperedges))

#nodes, hyperedges = read_movielens_mat_file()
#S, index_map = get_incidence_matrix(nodes, hyperedges)

#node_degrees = np.squeeze(np.asarray(sp.csr_matrix.sum(S, axis=1)))
#edge_degrees = np.squeeze(np.asarray(sp.csr_matrix.sum(S, axis=0)))

#node_degrees_mean = np.average(node_degrees)
#edge_degrees_mean = np.average(edge_degrees)

#print(node_degrees_mean)
#print(edge_degrees_mean)