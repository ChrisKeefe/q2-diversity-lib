# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import (Plugin)
# Q2_DIVERSITY:
# from qiime2.plugin import (Plugin, Str, Properties, Choices, Int, Bool, Range
#                          Float, Set, Visualization, Metadata, MetadataColumn,
#                           Categorical, Numeric, Citations)
import q2_diversity_lib


from qiime2.plugin import Citations
# Q2_DIVERSITY:
# from q2_types.feature_data import (FeatureData, Sequence, AlignedSequence,
#                                    Taxonomy)
# from q2_types.feature_table import (FeatureTable, Frequency)
# from q2_types.tree import Phylogeny, Rooted
# from q2_types.feature_table import FeatureTable, Frequency, RelativeFrequency
# from q2_types.distance_matrix import DistanceMatrix
# from q2_types.sample_data import AlphaDiversity, SampleData
# from q2_types.tree import Phylogeny, Rooted
# from q2_types.ordination import PCoAResults

citations = Citations.load('citations.bib', package='q2_diversity_lib')
plugin = Plugin(
    name='diversity-lib',
    version=q2_diversity_lib.__version__,
    website='https://github.com/qiime2/q2-diversity-lib',
    short_description=('Utility exposing diversity metrics as actions'),
    package='q2_diversity_lib',
    description=('Utility plugin exposing alpha- and beta-diversity metrics',
                 'as discrete Actions'),  # TODO expand? missing space?
    # user_support_text=('https://github.com/biocore/'
    #                    'q2-fragment-insertion/issues'),
)

plugin.methods.register_function(
    function=q2_diversity_lib.hello_world,
    inputs=None,
    parameters=None,
    outputs=None,
    input_descriptions=None,
    parameter_descriptions=None,
    output_descriptions=None,
    name='Hello World',
    description='HelloWorld: a Broad Greeting',
    citations=[citations['HelloWorld']]
)
