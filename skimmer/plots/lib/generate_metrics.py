import psycopg2
import scipy
import scipy.cluster.hierarchy
from jellyfish import *
import pickle
import numpy as np

UNASSIGNED_DEV_CLASS = 0x1F00
DB_HOST = 'localhost'
DB_USER = 'server'
DB_PASS = 'CutePuppies123!'
DB_NAME = 'skimmer'

class Nishants_Style_of_Record:
    def __init__(self, entry):

        self.MAC = entry[0]
        if entry[2]:
            self.geo_loc = [float(x) for x in entry[2][1:-1].split(',')]
        else:
            self.geo_loc = ''
        self.trunc_MAC = self.MAC[:8]
        self.dev_name = entry[1]

    def __str__(self):
        return ("LMAO YOU ACTUALLY THOUGHT THIS SHIT WOULD WORK????")

class Cluster_Util:
    def __init__(self):
        self.name_clusters = []
        self.gen_clusters()

    def gen_clusters(self):
        try:
            with open('name_clusters.pickle', 'rb') as handle:
                self.name_clusters = pickle.load(handle)
            return
        except Exception:
            pass

        conn = psycopg2.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, dbname=DB_NAME
        )
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT ON (devname,mac) devname, mac FROM " +
                    "enqresp WHERE devmajor = 31" +
                    " and devminor = 0 and devname != '';")
        nameMacPairs = cur.fetchall()
        devnames = [name for (name, mac) in nameMacPairs]

        # Define distance metric of jaro distance between strings
        def d(coord):
            i, j = coord
            return levenshtein_distance(devnames[i], devnames[j])

        # Use numpy.triu_indices to get the coordinates of the upper triangle:
        triu_indices = np.triu_indices(len(devnames), 1)

        # Use numpy.apply_along_axis to apply the distance function to the
        # coordinates of the upper triangle just computed:
        dist_res = np.apply_along_axis(d, 0, triu_indices)

        # Pass this array to scipy.cluster.hierarchy.linkage:
        cluster_tree = scipy.cluster.hierarchy.linkage(dist_res, 'ward')

        cutTree = scipy.cluster.hierarchy.fcluster(
            cluster_tree, t=3, criterion='distance')

        devListList = []
        for i in range(max(cutTree)):
            devList = []
            devListList.append(devList)
            for j in range(len(cutTree)):
                if cutTree[j] == i:
                    devList.append(j)
        devListList = list(enumerate(devListList))
        cutList = cutTree.tolist()
        devListList = sorted(devListList, key=lambda x: cutList.count(x[0]))
        for i in range(max(cutTree)):
            if cutTree.tolist().count(i):
                self.name_clusters.append(
                    [devnames[x] for x in devListList[i][1]]
                )

        cur.close()
        conn.close()

        with open('name_clusters.pickle', 'wb') as handle:
            pickle.dump(self.name_clusters, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def device_name_in_small_cluster(self, name):
        for cluster in self.name_clusters:
            if len(cluster) < 10 and name in cluster:
                return True
        return False

class Data_Manager:
    def __init__(self):
        self.entries = []

    def get_me_some_good_name_clusters_uh_huh_thats_what_im_talking_about(self, cur, query):
        cur.execute(query)
        for entry in cur.fetchall():
            self.entries.append(Nishants_Style_of_Record(entry))

        THAT_GOOD_OL_CLUSTER_UTIL = Cluster_Util()

        Int_Result = 0

        for entry in self.entries:
            if THAT_GOOD_OL_CLUSTER_UTIL.device_name_in_small_cluster(entry.dev_name):
                print(entry.dev_name, "ODD")
                Int_Result += 1
            else:
                print(entry.dev_name, "EVEN")


        return Int_Result
