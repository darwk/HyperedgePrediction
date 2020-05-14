import pickle

from dataset_utils.citation_network import get_largest_cc


def get_dblp_network(dataset_folder):
    dblpfile = open(dataset_folder + '/dblp.pickle', 'rb')
    dblp_dataset = pickle.load(dblpfile)

    intralayers = dblp_dataset['intra']

    hyperedges = []
    for i in range(len(intralayers)):
        hyperedge_info = intralayers[i]

        head_set = set(hyperedge_info[0])
        tail_set = set(hyperedge_info[1])

        hyperedge = list(head_set | tail_set)
        hyperedge.sort()
        hyperedges.append(hyperedge)

    nodes = set([])
    for i in range(len(hyperedges)):
        nodes.update(hyperedges[i])
    nodes = list(nodes)
    nodes.sort()

    nodes, hyperedges = get_largest_cc(nodes, hyperedges)

    print("Total number of nodes - " + str(len(nodes)))
    print("Total number of hyperedges - " + str(len(hyperedges)))

    return nodes, hyperedges


