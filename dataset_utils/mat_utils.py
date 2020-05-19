import os
import numpy as np
import scipy.io as sio

from dataset_utils.amazon_network import get_amazon_network
from dataset_utils.citation_network import get_citation_network
from dataset_utils.coreference_network import get_coreference_network
from dataset_utils.dblp_network import get_dblp_network
from dataset_utils.twitter_network import get_twitter_network
from hypergraph_utils import get_incidence_matrix


def store_as_mat(dataset, network):
    dataset_folder = os.getcwd() + "/Raw_Datasets"

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

    S, index_map = get_incidence_matrix(nodes, hyedges)

    output_folder = os.getcwd() + "/Datasets/"
    file_name = dataset
    if network != "":
        file_name += "_" + network

    sio.savemat(output_folder + file_name, {"S": S, "index_map": index_map})


store_as_mat("cora", "cocitation")
