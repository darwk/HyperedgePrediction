import os

from dataset_utils.amazon_network import get_amazon_network
from dataset_utils.citation_network import get_citation_network
from dataset_utils.coreference_network import get_coreference_network
from dataset_utils.dblp_network import get_dblp_network
from dataset_utils.twitter_network import get_twitter_network


def get_network(dataset, network):

    dataset_folder = os.getcwd() + "/Datasets"

    if dataset == "citeseer" or dataset == "cora" or dataset == "aminer":
        if network == "cocitation":
            nodes, hyedges, paperid_classid, classid_classname = get_citation_network(dataset, dataset_folder)
        elif network == "coreference":
            nodes, hyedges, paperid_classid, classid_classname = get_coreference_network(dataset, dataset_folder)
    elif dataset == "dblp":
        nodes, hyedges = get_dblp_network(dataset_folder)
    elif dataset == "twitter":
        nodes, hyedges = get_twitter_network(1000, dataset_folder)
    elif dataset == "amazon":
        nodes, hyedges = get_amazon_network(network, dataset_folder)

    return nodes, hyedges

