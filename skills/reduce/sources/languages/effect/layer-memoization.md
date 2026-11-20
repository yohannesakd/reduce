# Layer Memoization

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/requirements-management/layer-memoization/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
Layer memoization allows a layer to be created once and used multiple times in the dependency graph. If we use the same layer twice:

then the L1 layer will be allocated only once.

Memoization When Providing Globally

One important feature of an Effect application is that layers are shared by default. This means that if the same layer is used twice, and if we provide the layer globally, the layer will only be allocated a single time. For every layer in our dependency graph, there is only one instance of it that is shared between all the layers that depend on it.

Example

For example, assume we have the three services A, B, and C. The implementation of both B and C is dependent on the A service:

Although both BLive and CLive layers require the ALive layer, the ALive layer is instantiated only once. It is shared with both BLive and CLive.

Acquiring a Fresh Version

If we don’t want to share a module, we should create a fresh, non-shared version of it through Layer.fresh.

Example

No Memoization When Providing Locally

If we don’t provide a layer globally but instead provide them locally, that layer doesn’t support memoization by default.

Example

In the following example, we provided the ALive layer two times locally, and Effect doesn’t memoize the construction of the ALive layer.
So, it will be initialized two times:

Manual Memoization

We can memoize a layer manually using a Layer.MemoMap. A MemoMap tracks which layers have already been built so that building the same layer again, against the same MemoMap, reuses the earlier result instead of re-running its acquisition effect.

Create a MemoMap with Layer.makeMemoMap, then build a layer into a Context with Layer.buildWithMemoMap, passing the MemoMap and a Scope.
