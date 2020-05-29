So `pielou` and `shannon` can both filter NaNs now (at the user's discretion). Are there justifiable use cases where users might want to use these functions to filter "zero"/feature-less samples, when undefined values are not in play? 

Evan: No. 

Simplistic example: do we let people opt in to drop "zero" samples in `observed_otus`? This seems like a reasonable convenience, I just don't know whether it actually benefits users. 

Evan: No.

Are you aware of any actions that require or benefit from having a complete picture of the (unfiltered) data set? Put differently, in a perfect world is there value in programatically attaching properties to restrict the downstream use of these filtered alpha-diversity vectors? (e.g. `samples-filtered-0`, or `samples-filtered-lt2`)

Evan: No.

Another consideration - is it worth including a note in the `drop_undefined_samples` or `drop_zeros` parameter description indicating that users will have to filter their table to match for predictable downstream use (e.g. in q2-longitudinal)?

Evan: No. Generally, tables that are a superset of the samples in a vector are not problematic. 

Finally, these filters would be irrelevant to any rarefaction-based pipeline (like `core-metrics`). What are the politics and cost-benefit of producing a similar pipeline that uses simple proportional normalization? And if we did, I assume we would hide the `drop_undefined_samples` parameter there, so we don't have to produce filtered tables for each level of filteration (e.g. `pielou` requires two or more features per sample to avoid NaNs, while `shannon` only needs one)?

Evan: No. These methods allow people to do this stuff, but we are not currently in the business of encouraging this approach for naive users by building pipelines. 
