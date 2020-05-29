1.
TODO: `skbio/diversity/_util` contains many other errors that reference otu_ids or trees. Some errors like this are masked in faith_pd()
Are these worth catching and modifying more broadly?

If so, these should also be tested, as in test_alpha.py:
```
def test_faith_pd_error_rewriting(self):
    tree = skbio.TreeNode.read(io.StringIO(
        '((A:0.3):0.2, C:100)root;'))
    with self.assertRaisesRegex(skbio.tree.MissingNodeError,
                                'feature_ids.*phylogeny'):
        faith_pd(table=self.input_table, phylogeny=tree)
```

2.
NOTE: q2-diversity's implementation of pielou_e cast all table members to int. This was breaking RelativeFrequency tables, and has been removed. It does not
appear to negatively impact calculations (b/c floating pt), but has seen limited testing on large dense matrices.

3.
NOTE: biom tables are row = feature, col = sample.
In most actions, they are tranformed into numpy ndarrays, where row=sample, col=feature

4.
NOTE: Pielou `drop_undefined_samples` default set to False, b/c skbio currently retains nan-value samples (e.g. single-feature samples)

5.
NOTE: `drop_undefined_samples` renamed to `drop_undefined_samples` to alleviate caps-related errors. Lowercase will be required by the framework in future.

6.
NOTE: `counts` may not be the best name to apply to tables that may also contain relative frequency data (e.g. shannon, pielou)
Discussed with Matt - counts is a solid name

7.
TODO: consider whether the SKbio driver functions need any direct testing.

8.
DONE: Get a live list of public q2_diversity_lib functions in the testing file (like the list you get from .__all__). Iterate over these functions, passing empty lists and trees where necessary, to DRY up the empty-list testing.

This may be useful: https://stackoverflow.com/a/34452/9872253. NOTE: Evan recommends a static list instead of something programatically generated, as this has bitten him repeatedly. Extreme care in testing if this is the approach I take.

This has been handled by making the empty-list guard a decorator, reducing duplication a bunch without having to iterate over functions as data.

9.
REMOVED: If `drop_undefined_samples` is selected, programatically add a property like "samples_filtered" to the output?~
Discussed with Evan on 7/17, deemed not useful.

10.
DONE: change non_zero_elements_per_sample to nonzero_elements_per_sample

11.
DONE: alpha-diversity metric descriptions: change "for all samples in a" to "for each sample in a"

12.
DONE: refactor drop_undefined_samples into a private helper function called in the public methods

13.
NOTE: Did not create a list of phylogenetic alpha diversity measures in tests, because there is only one. Faith_PD is tested independently.

14. 
Note: 
Dropped `% Properties('phylogenetic')` from Unifrac Distance Matrices after discussion with Evan

15. 
TODO: Add Jaccard Similarity and (similarity matrix type?) https://github.com/qiime2/q2-diversity/issues/163

16.
TODO: Is this a thing we care about for Bray-Curtis? It doesn't seem necessary, and I'm not sure a simplification/optimization is worth complicating things, especially if we are unlikely to have matching specimen counts across samples.
"The index can be simplified to 1-2C/2 = 1-C when the abundances at each site are expressed as proportions, though the two forms of the equation only produce matching results when the total number of specimens counted at both sites are the same. Further treatment can be found in Legendre & Legendre.[2]"
- wikipedia


17. TODO: next! Add drop_undefined_values function/guards to beta diversity
functions, and tests.

18. TODO: next! Add variance_adjusted_unweighted_unifrac as an independent method. Unweighted unifrac should be able to take presence absence tables, but Unifrac.unweighted exposes a variance_adjusted parameter which
weights distances on the proportion of the relative abundance represented between the samples at a node under evaluation. (Chang et al) So, we'll restrict standard unweighted to not using variance_adjusted, and variance_adjusted_unweighted_unifrac will disallow presence/absence tables

19. TODO: next! Add variance_adjusted_weighted_unifrac as an independent method? See #18.
Note - registration descriptions will be available in the base functions at the head of the draft_fancy_unifracs branch

20. TODO: test bypass_tips arg to unifracs?