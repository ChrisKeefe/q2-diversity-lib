# ----------------------------------------------------------------------------
# Copyright (c) 2018-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import biom
import skbio.diversity
import sklearn.metrics
import unifrac


from q2_types.feature_table import BIOMV210Format
from q2_types.tree import NewickFormat
from ._util import (_disallow_empty_tables,
                    _safely_constrain_n_jobs)


# --------------------Non-Phylogenetic-----------------------
@_disallow_empty_tables
@_safely_constrain_n_jobs
def bray_curtis(table: biom.Table, n_jobs: int = 1) -> skbio.DistanceMatrix:
    counts = table.matrix_data.toarray().T
    sample_ids = table.ids(axis='sample')
    return skbio.diversity.beta_diversity(
        metric='braycurtis',
        counts=counts,
        ids=sample_ids,
        validate=True,
        pairwise_func=sklearn.metrics.pairwise_distances,
        n_jobs=n_jobs
    )


@_disallow_empty_tables
@_safely_constrain_n_jobs
def jaccard(table: biom.Table, n_jobs: int = 1) -> skbio.DistanceMatrix:
    counts = table.matrix_data.toarray().T
    sample_ids = table.ids(axis='sample')
    return skbio.diversity.beta_diversity(
        metric='jaccard',
        counts=counts,
        ids=sample_ids,
        validate=True,
        pairwise_func=sklearn.metrics.pairwise_distances,
        n_jobs=n_jobs
    )


# ------------------------Phylogenetic-----------------------
@_disallow_empty_tables
@_safely_constrain_n_jobs
def unweighted_unifrac(table: BIOMV210Format,
                       phylogeny: NewickFormat,
                       n_jobs: int = 1,
                       bypass_tips: bool = False) -> skbio.DistanceMatrix:
    f = unifrac.unweighted
    return f(str(table), str(phylogeny), threads=n_jobs,
             variance_adjusted=False, bypass_tips=bypass_tips)


@_disallow_empty_tables
@_safely_constrain_n_jobs
def weighted_unifrac(table: BIOMV210Format,
                     phylogeny: NewickFormat,
                     n_jobs: int = 1,
                     bypass_tips: bool = False) -> skbio.DistanceMatrix:
    f = unifrac.weighted_unnormalized
    return f(str(table), str(phylogeny), threads=n_jobs,
             variance_adjusted=False, bypass_tips=bypass_tips)


@_disallow_empty_tables
@_safely_constrain_n_jobs
def weighted_normalized_unifrac(
        table: BIOMV210Format, phylogeny: NewickFormat,
        n_jobs: int = 1, variance_adjusted: bool = False,
        bypass_tips: bool = False) -> skbio.DistanceMatrix:
    f = unifrac.weighted_normalized
    return f(str(table), str(phylogeny), threads=n_jobs,
             variance_adjusted=variance_adjusted, bypass_tips=bypass_tips)


@_disallow_empty_tables
@_safely_constrain_n_jobs
def generalized_unifrac(table: BIOMV210Format, phylogeny: NewickFormat,
                        n_jobs: int = 1, alpha: float = 1.0,
                        variance_adjusted: bool = False,
                        bypass_tips: bool = False) -> skbio.DistanceMatrix:
    f = unifrac.generalized
    # TODO: Is the unifrac.generalized warning handled appropriately?
    # It should reach the user. If it doesn't, maybe catch it and provide
    # output a la https://stackoverflow.com/a/15934081. Probably overdoing it.
    # Maybe better to just check the value of alpha, report our own warning?
    return f(str(table), str(phylogeny), threads=n_jobs, alpha=alpha,
             variance_adjusted=variance_adjusted, bypass_tips=bypass_tips)
