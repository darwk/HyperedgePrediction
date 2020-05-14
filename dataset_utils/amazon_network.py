import scipy.io


def get_amazon_network(network_type, dataset_folder):

    if network_type == "copurchase":
        mat = scipy.io.loadmat(dataset_folder + "/copurchase.mat")
        network = mat['copurchase'][0, 0]

    elif network_type == "coview":
        mat = scipy.io.loadmat(dataset_folder + "/coview.mat")
        network = mat['coview'][0, 0]

    nodes = set([])
    hyperedges = []

    for i in range(len(network)):
        hyperedge = network[i][0]

        hyperedges.append(hyperedge)
        nodes.update(set(hyperedge))

    nodes = list(nodes)
    nodes.sort()

    return nodes, hyperedges
