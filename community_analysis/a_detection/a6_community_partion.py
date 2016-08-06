import __init__

from community_analysis.__init__ import la_dir, pg_dir

import community
import networkx as nx

from taxi_common.file_handling_functions import load_pickle_file, get_all_files, check_dir_create

MIN_AN_DAYS = 23


def run():
    yyyy = '2009'
    print 'start',
    assert len(get_all_files(la_dir, '', '.pkl')) == 1
    fn = get_all_files(la_dir, '', '.pkl').pop()
    print fn
    print 'pkl file loading ...'
    pairs_day_counting = load_pickle_file('%s/%s' % (la_dir, fn))
    print 'finished'
    print 'Graph constructing ...'
    G = nx.Graph()
    for (k0, k1), num_days in pairs_day_counting.iteritems():
        if num_days < MIN_AN_DAYS:
            continue
        G.add_edge(k0, k1, weight=num_days)

    del pairs_day_counting
    pg_th_dir = '%s/%s-TH(%d)' % (pg_dir, yyyy, MIN_AN_DAYS); check_dir_create(pg_th_dir)
    print 'finished'
    print 'Whole graph pickling ...'
    nx.write_gpickle(G, '%s/%s-TH(%d)-whole.pkl' % (pg_th_dir, yyyy, MIN_AN_DAYS))
    print 'finished'
    # first compute the best partition
    print 'Partitioning ...'
    partition = community.best_partition(G)
    print 'finished'
    # drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        # read_gpickle(path)
        print count, 'Saving sub-graph ...'
        nx.write_gpickle(G.subgraph(list_nodes), '%s/%s-TH(%d)-PD(%d).pkl' % (pg_dir, yyyy, MIN_AN_DAYS, count))
        print 'finished'
        # G.edges()
        # nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
        #                        node_color=str(count / size), with_labels=True)
    # print 'node drawing finished'
    # nx.draw_networkx_edges(G, pos, alpha=0.5)
    # print 'edge drawing finished'
    # plt.show()





if __name__ == '__main__':
    from traceback import format_exc

    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise