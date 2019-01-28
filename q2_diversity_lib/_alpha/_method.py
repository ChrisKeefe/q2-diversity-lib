# ----------------------------------------------------------------------------
# Copyright (c) 2018-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import biom
import pandas as pd
import skbio.diversity

# def hello_world() -> str:
#     dummy_string = "Hello World!"
#     print(dummy_string)
#     return dummy_string

# We should consider moving these functions to scikit-bio. They're part of
# the private API here for now.


# def non_phylogenetic_metrics():
#     return {'ace', 'chao1', 'chao1_ci', 'berger_parker_d', 'brillouin_d',
#             'dominance', 'doubles', 'enspie', 'esty_ci', 'fisher_alpha',
#             'goods_coverage', 'heip_e', 'kempton_taylor_q', 'margalef',
#             'mcintosh_d', 'mcintosh_e', 'menhinick', 'michaelis_menten_fit',
#             'observed_otus', 'osd', 'pielou_e', 'robbins', 'shannon',
#             'simpson', 'simpson_e', 'singles', 'strong', 'gini_index',
#             'lladser_pe', 'lladser_ci'}


def faith_pd(table: biom.Table, phylogeny: skbio.TreeNode) -> pd.Series:
    if table.is_empty():
        raise ValueError("The provided table object is empty")

    counts = table.matrix_data.toarray().astype(int).T
    sample_ids = table.ids(axis='sample')
    feature_ids = table.ids(axis='observation')

    try:
        result = skbio.diversity.alpha_diversity(metric='faith_pd',
                                                 counts=counts,
                                                 ids=sample_ids,
                                                 otu_ids=feature_ids,
                                                 tree=phylogeny)
    except skbio.tree.MissingNodeError as e:
        message = str(e).replace('otu_ids', 'feature_ids')
        message = message.replace('tree', 'phylogeny')
        raise skbio.tree.MissingNodeError(message)

    result.name = 'faith_pd'
    return result


# def alpha(table: biom.Table, metric: str) -> pd.Series:
#     if metric not in non_phylogenetic_metrics():
#         raise ValueError("Unknown metric: %s" % metric)
#     if table.is_empty():
#         raise ValueError("The provided table object is empty")
#
#     counts = table.matrix_data.toarray().astype(int).T
#     sample_ids = table.ids(axis='sample')
#
#     result = skbio.diversity.alpha_diversity(metric=metric, counts=counts,
#                                              ids=sample_ids)
#     result.name = metric
#     return result
