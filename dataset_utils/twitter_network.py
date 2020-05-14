from dataset_utils.citation_network import get_largest_cc


def get_twitter_network(no_nodes, dataset_folder):
    higgsfile = open(dataset_folder + '/higgs-social_network.edgelist', 'r')

    hypergraph = {}
    for line in higgsfile.readlines():
        temp = line.split("\n")
        link = temp[0].split(" ")

        head = int(link[0])
        tail = int(link[1])

        if tail not in hypergraph.keys():
            hypergraph[tail] = []

        hypergraph[tail].append(head)

    keys = list(hypergraph.keys())
    keys.sort()

    trunc_nodes = keys[0:no_nodes]

    hyperedges = []
    for node in trunc_nodes:
        hyperedge = hypergraph[node]
        new_hyperedge = []
        for i in range(len(hyperedge)):
            if hyperedge[i] in trunc_nodes:
                new_hyperedge.append(hyperedge[i])

        if len(new_hyperedge) >= 2:
            hyperedges.append(new_hyperedge)

    updated_nodes = set([])
    for hyperedge in hyperedges:
        updated_nodes.update(hyperedge)

    updated_nodes = list(updated_nodes)
    updated_nodes.sort()

    updated_nodes, hyperedges = get_largest_cc(updated_nodes, hyperedges)

    updated_nodes = list(updated_nodes)
    updated_nodes.sort()

    return updated_nodes, hyperedges