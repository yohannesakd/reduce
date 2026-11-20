# Comfy-Org/ComfyUI_frontend commit 073237b79c

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Simon Pinfold
- Date: 2026-09-25
- Original location: https://github.com/Comfy-Org/ComfyUI_frontend/commit/073237b79c7547f5e1550d9cf4b1b74884bffbfe
- Copied: 2026-11-20, from the commit data and diff of the GitHub API

## Text
refactor(model-library): reload through one debounced watcher on the capability flags

Both capability flags arrive in the same handshake, so one watcher on
both schedules the existing debounced reload (renamed from the scan-only
name) instead of two watchers each starting an immediate reload. The
debounce lets an eager load started on the flag flip get picked up by
the reload rather than finishing into replaced folders.

## Diff

````diff
diff --git a/src/stores/modelStore.test.ts b/src/stores/modelStore.test.ts
index 2bfa39f1471..886f32d2256 100644
--- a/src/stores/modelStore.test.ts
+++ b/src/stores/modelStore.test.ts
@@ -1,11 +1,10 @@
 import { beforeEach, describe, expect, it, vi } from 'vitest'
-import { nextTick, reactive, watch } from 'vue'
+import { reactive, watch } from 'vue'
 
 import { useFeatureFlags } from '@/composables/useFeatureFlags'
 import { assetService } from '@/platform/assets/services/assetService'
 import type * as DistributionTypes from '@/platform/distribution/types'
 import { remoteConfig } from '@/platform/remoteConfig/remoteConfig'
-import { reportError } from '@/platform/telemetry/reportError'
 import { api } from '@/scripts/api'
 import {
   ResourceState,
@@ -23,8 +22,6 @@ vi.mock(import('@/platform/distribution/types'), () => mockDistribution)
 
 vi.mock(import('@/platform/remoteConfig/remoteConfig'))
 
-vi.mock(import('@/platform/telemetry/reportError'))
-
 const featureState = vi.hoisted(() => ({
   serverFeatures: {} as Record<string, unknown>
 }))
@@ -644,12 +641,14 @@ describe('useModelStore', () => {
       expect(names).toContain('0/asset-only.safetensors')
       expect(names).not.toContain('0/sdxl.safetensors')
     })
+  })
 
-    it('eagerly loads the rebuilt folders when a watcher registered after the store loads on the flag flip', async () => {
+  describe('capability handshake', () => {
+    it('reloads once for both flags and re-loads the folders an eager load started', async () => {
+      vi.useFakeTimers()
       enableMocks(false)
       store = useModelStore()
       await store.loadModelFolders()
-
       const { flags } = useFeatureFlags()
       const eagerLoads: Promise<unknown>[] = []
       watch(
@@ -660,188 +659,18 @@ describe('useModelStore', () => {
       )
 
       featureState.serverFeatures.assets = true
-      await vi.waitFor(() => expect(eagerLoads).toHaveLength(1))
+      remoteConfig.value = { supports_model_type_tags: true }
+      await vi.advanceTimersByTimeAsync(1000)
       await Promise.all(eagerLoads)
 
+      expect(api.getModelFolders).toHaveBeenCalledTimes(2)
       expect(store.modelFolders.map((folder) => folder.state)).toStrictEqual([
         ResourceState.Loaded,
         ResourceState.Loaded
       ])
-      expect(api.getModels).not.toHaveBeenCalled()
-      expect(assetService.getAssetModels).toHaveBeenCalledTimes(2)
-    })
-
-    it('eagerly loads the rebuilt folders when a load starts mid-rebuild', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      const folders = await api.getModelFolders()
-      let releaseRebuild!: () => void
-      vi.mocked(api.getModelFolders).mockReturnValueOnce(
-        new Promise((resolve) => {
-          releaseRebuild = () => resolve(folders)
-        })
-      )
-
-      featureState.serverFeatures.assets = true
-      await vi.waitFor(() =>
-        expect(api.getModelFolders).toHaveBeenCalledTimes(3)
-      )
-      const eagerLoad = store.loadModels()
-      releaseRebuild()
-      await eagerLoad
-
-      expect(store.modelFolders.map((folder) => folder.state)).toStrictEqual([
-        ResourceState.Loaded,
-        ResourceState.Loaded
-      ])
-      expect(api.getModels).not.toHaveBeenCalled()
-    })
-
-    it('reads the rebuilt folder when a read starts mid-rebuild', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      const folders = await api.getModelFolders()
-      let releaseRebuild!: () => void
-      vi.mocked(api.getModelFolders).mockReturnValueOnce(
-        new Promise((resolve) => {
-          releaseRebuild = () => resolve(folders)
-        })
-      )
-
-      featureState.serverFeatures.assets = true
-      await vi.waitFor(() =>
-        expect(api.getModelFolders).toHaveBeenCalledTimes(3)
-      )
-      const read = store.getLoadedModelFolder('checkpoints')
-      releaseRebuild()
-      const folder = await read
-
-      expect(folder).toBe(store.modelFolders[0])
-      expect(folder!.state).toBe(ResourceState.Loaded)
-      expect(api.getModels).not.toHaveBeenCalled()
-    })
-
-    it('keeps the committed folders when a superseded capability reload fails', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      const bootFolder = store.modelFolders[0]
-      let failSupersededReload!: () => void
-      vi.mocked(api.getModelFolders).mockReturnValueOnce(
-        new Promise((_, reject) => {
-          failSupersededReload = () => reject(new Error('offline'))
-        })
-      )
-
-      featureState.serverFeatures.assets = true
-      remoteConfig.value = { supports_model_type_tags: true }
-      await vi.waitFor(() => expect(store.modelFolders[0]).not.toBe(bootFolder))
-      failSupersededReload()
-      await vi.waitFor(() => expect(reportError).toHaveBeenCalled())
-      await store.loadModels()
-
-      expect(api.getModelFolders).toHaveBeenCalledTimes(3)
-      expect(api.getModels).not.toHaveBeenCalled()
-    })
-
-    it('reads an asset-backed folder in the same tick as the flag flip', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-
-      featureState.serverFeatures.assets = true
-      const folder = await store.getLoadedModelFolder('checkpoints')
-
-      expect(folder).toBe(store.modelFolders[0])
-      expect(folder!.state).toBe(ResourceState.Loaded)
-      expect(api.getModels).not.toHaveBeenCalled()
       expect(assetService.getAssetModels).toHaveBeenCalledWith('checkpoints')
-    })
-
-    it('rebuilds from the asset source on the next load after the capability reload and a newer refresh both fail', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      let failCapabilityReload!: () => void
-      vi.mocked(api.getModelFolders)
-        .mockReturnValueOnce(
-          new Promise((_, reject) => {
-            failCapabilityReload = () => reject(new Error('offline'))
-          })
-        )
-        .mockRejectedValueOnce(new Error('offline'))
-
-      featureState.serverFeatures.assets = true
-      await vi.waitFor(() =>
-        expect(api.getModelFolders).toHaveBeenCalledTimes(2)
-      )
-      await expect(store.refresh()).rejects.toThrow('offline')
-      failCapabilityReload()
-      await vi.waitFor(() => expect(reportError).toHaveBeenCalled())
-      await store.loadModels()
-
-      expect(store.modelFolders.map((folder) => folder.state)).toStrictEqual([
-        ResourceState.Loaded,
-        ResourceState.Loaded
-      ])
-      expect(api.getModels).not.toHaveBeenCalled()
-    })
-
-    it('rebuilds from the asset source on the next load after the capability reload fails', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      vi.mocked(api.getModelFolders).mockRejectedValueOnce(new Error('offline'))
-
-      featureState.serverFeatures.assets = true
-      await vi.waitFor(() =>
-        expect(reportError).toHaveBeenCalledWith(expect.any(Error), {
-          errorType: 'model_library_capability_reload'
-        })
-      )
-      await store.loadModels()
-
-      expect(store.modelFolders.map((folder) => folder.state)).toStrictEqual([
-        ResourceState.Loaded,
-        ResourceState.Loaded
-      ])
-      expect(api.getModels).not.toHaveBeenCalled()
-      expect(assetService.getAssetModels).toHaveBeenCalledTimes(2)
-    })
-
-    it('reloads every loaded folder from the asset source when a read follows a failed capability reload', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModels()
-      vi.mocked(api.getModelFolders).mockRejectedValueOnce(new Error('offline'))
-
-      featureState.serverFeatures.assets = true
-      await vi.waitFor(() => expect(reportError).toHaveBeenCalled())
-      await store.getLoadedModelFolder('checkpoints')
-
-      expect(store.modelFolders.map((folder) => folder.state)).toStrictEqual([
-        ResourceState.Loaded,
-        ResourceState.Loaded
-      ])
       expect(assetService.getAssetModels).toHaveBeenCalledWith('vae')
     })
-
-    it('rebuilds from the asset source on the next folder read after the capability reload fails', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      vi.mocked(api.getModelFolders).mockRejectedValueOnce(new Error('offline'))
-
-      featureState.serverFeatures.assets = true
-      await vi.waitFor(() => expect(reportError).toHaveBeenCalled())
-      const folder = await store.getLoadedModelFolder('checkpoints')
-
-      expect(folder!.state).toBe(ResourceState.Loaded)
-      expect(api.getModels).not.toHaveBeenCalled()
-      expect(assetService.getAssetModels).toHaveBeenCalledWith('checkpoints')
-    })
   })
 
   describe('model-type capability change', () => {
@@ -880,21 +709,6 @@ describe('useModelStore', () => {
       })
       expect(assetService.invalidateModelBuckets).toHaveBeenCalled()
     })
-
-    it('does not reload on the legacy listing path', async () => {
-      enableMocks(false)
-      store = useModelStore()
-      await store.loadModelFolders()
-      await store.getLoadedModelFolder('checkpoints')
-      expect(api.getModelFolders).toHaveBeenCalledTimes(1)
-
-      remoteConfig.value = { supports_model_type_tags: true }
-
-      await nextTick()
-      await nextTick()
-      expect(api.getModelFolders).toHaveBeenCalledTimes(1)
-      expect(assetService.invalidateModelBuckets).not.toHaveBeenCalled()
-    })
   })
 
   describe('visibleModelFolders', () => {
diff --git a/src/stores/modelStore.ts b/src/stores/modelStore.ts
index 0ee47e19fa0..d7858b85cb1 100644
--- a/src/stores/modelStore.ts
+++ b/src/stores/modelStore.ts
@@ -6,7 +6,6 @@ import { useFeatureFlags } from '@/composables/useFeatureFlags'
 import type { ModelFile } from '@/platform/assets/schemas/assetSchema'
 import { assetService } from '@/platform/assets/services/assetService'
 import { isCloud } from '@/platform/distribution/types'
-import { reportError } from '@/platform/telemetry/reportError'
 import { api } from '@/scripts/api'
 
 /** (Internal helper) finds a value in a metadata object from any of a list of keys. */
@@ -314,8 +313,6 @@ export const useModelStore = defineStore('models', () => {
   }
 
   let modelFoldersRequestId = 0
-  const pendingReloads = new Set<Promise<boolean>>()
-  let committedAssetsEnabled: boolean | undefined
 
   /**
    * Whether anything has consumed this store's model data (sidebar loads,
@@ -328,7 +325,6 @@ export const useModelStore = defineStore('models', () => {
     requestId: number
     names: string[]
     folders: Record<string, ModelFolder>
-    assetsEnabled: boolean
   }
 
   /**
@@ -356,22 +352,12 @@ export const useModelStore = defineStore('models', () => {
         flags.assetsEnabled ? effectiveModelExtensions(folder.extensions) : []
       )
     }
-    return {
-      requestId,
-      names: resData.map((folder) => folder.name),
-      folders,
-      assetsEnabled: flags.assetsEnabled
-    }
+    return { requestId, names: resData.map((folder) => folder.name), folders }
   }
 
-  function commitModelFolders({
-    names,
-    folders,
-    assetsEnabled
-  }: PreparedModelFolders): void {
+  function commitModelFolders({ names, folders }: PreparedModelFolders): void {
     modelFolderNames.value = names
     modelFolderByName.value = folders
-    committedAssetsEnabled = assetsEnabled
   }
 
   /** Loads the model folder structure from the server; false when superseded. */
@@ -382,28 +368,10 @@ export const useModelStore = defineStore('models', () => {
     return true
   }
 
-  async function ensureCurrentModelFolders() {
-    // A superseded rebuild commits nothing; bounded retry until one commits.
-    for (let attempt = 0; attempt < 3; attempt++) {
-      // Folders a pending reload replaces would finish loading into detached objects.
-      while (pendingReloads.size > 0) await Promise.allSettled(pendingReloads)
-      const current =
-        modelFolderNames.value.length > 0 &&
-        committedAssetsEnabled === flags.assetsEnabled
-      if (current) return
-      const rebuilt =
-        modelFolderNames.value.length > 0
-          ? await reloadModels()
-          : await loadModelFolders()
-      if (rebuilt) return
-    }
-  }
-
   async function getLoadedModelFolder(
     folderName: string
   ): Promise<ModelFolder | null> {
     modelDataConsumed = true
-    await ensureCurrentModelFolders()
     const folder = Object.hasOwn(modelFolderByName.value, folderName)
       ? modelFolderByName.value[folderName]
       : undefined
@@ -418,7 +386,14 @@ export const useModelStore = defineStore('models', () => {
    */
   async function loadModels() {
     modelDataConsumed = true
-    await ensureCurrentModelFolders()
+    // A load superseded by a newer concurrent one commits nothing, which
+    // would leave the folder list empty and silently load no models; retry
+    // until a load of ours commits (even a genuinely empty result) or a
+    // concurrent one has populated the list. Bounded as a safety net.
+    for (let attempt = 0; attempt < 3; attempt++) {
+      if (modelFolderNames.value.length > 0) break
+      if (await loadModelFolders()) break
+    }
     return Promise.all(modelFolders.value.map((folder) => folder.load()))
   }
 
@@ -469,16 +444,6 @@ export const useModelStore = defineStore('models', () => {
    * one — the winning load populates the fresh data.
    */
   async function reloadModels(): Promise<boolean> {
-    const reload = rebuildModelFolders()
-    pendingReloads.add(reload)
-    try {
-      return await reload
-    } finally {
-      pendingReloads.delete(reload)
-    }
-  }
-
-  async function rebuildModelFolders(): Promise<boolean> {
     assetService.invalidateModelBuckets()
     // Loading counts as previously loaded: a scan-complete reload can land
     // while the eager load is still in flight, and replacing those folder
@@ -533,19 +498,18 @@ export const useModelStore = defineStore('models', () => {
   }
 
   /**
-   * Scan completions arrive as one event per scanned root and can land in
-   * bursts; coalesce them into one trailing reload instead of one full
-   * library walk per event.
+   * Scan completions and capability changes can land in bursts; coalesce
+   * them into one trailing reload instead of one full library walk per event.
    */
-  const SCAN_RELOAD_DEBOUNCE_MS = 500
+  const MODEL_RELOAD_DEBOUNCE_MS = 500
 
-  const reloadAfterScan = debounce(async () => {
+  const scheduleModelReload = debounce(async () => {
     try {
       await reloadModels()
     } catch (error) {
-      console.error('Failed to reload the model library after a scan', error)
+      console.error('Failed to reload the model library', error)
     }
-  }, SCAN_RELOAD_DEBOUNCE_MS)
+  }, MODEL_RELOAD_DEBOUNCE_MS)
 
   const unsubscribeModelsScanned = assetService.onModelsScanned(() => {
     // A scan changes bucket contents even when no UI has read this store
@@ -553,10 +517,10 @@ export const useModelStore = defineStore('models', () => {
     // skip the reload nothing is displaying.
     assetService.invalidateModelBuckets()
     if (!modelDataConsumed) return
-    reloadAfterScan()
+    scheduleModelReload()
   })
   onScopeDispose(() => {
-    reloadAfterScan.cancel()
+    scheduleModelReload.cancel()
     unsubscribeModelsScanned()
   })
 
@@ -564,23 +528,9 @@ export const useModelStore = defineStore('models', () => {
    * The WS `feature_flags` handshake can land after createGetModelsFunc()
    * already captured its data-source choice at store-init time, so a flag
    * flip after boot must force a reload to switch the sidebar's source.
-   *
-   * One handshake carrying both `assetsEnabled` and `supportsModelTypeTags`
-   * fires both watchers, issuing two concurrent reloadModels() calls. That is
-   * safe by design: prepareModelFolders()'s request-id discipline makes the
-   * stale response a no-op, so no debouncing is needed here.
    */
-  function reloadForCapabilityChange() {
-    reloadModels().catch((error) => {
-      reportError(error, { errorType: 'model_library_capability_reload' })
-    })
-  }
-
-  watch(() => flags.assetsEnabled, reloadForCapabilityChange)
-
-  watch(
-    () => flags.supportsModelTypeTags,
-    () => flags.assetsEnabled && reloadForCapabilityChange()
+  watch([() => flags.assetsEnabled, () => flags.supportsModelTypeTags], () =>
+    scheduleModelReload()
   )
 
   return {

````
