# openclaw/openclaw compare 0a0a2e0489026b2e73d139383e7b60515fcaf7f3...7745effd839d26863d8480c1888715841523c808

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: openclaw
- Original location: https://github.com/openclaw/openclaw/compare/0a0a2e0489026b2e73d139383e7b60515fcaf7f3...7745effd839d26863d8480c1888715841523c808
- Copied: 2026-11-20, from the commit data and diff of the GitHub API

## Text
- b231790955 refactor(worker-transport): remove redundant guards and helpers
- 7745effd83 chore: merge main to narrow worker transport cleanup

## Diff

````diff
diff --git a/src/gateway/worker-environments/node-desktop-carrier.ts b/src/gateway/worker-environments/node-desktop-carrier.ts
index b053d3f512831..728b250a73671 100644
--- a/src/gateway/worker-environments/node-desktop-carrier.ts
+++ b/src/gateway/worker-environments/node-desktop-carrier.ts
@@ -68,18 +68,12 @@ function isBindingCurrent(
   );
 }
 
-function invocationError(
-  result: Awaited<ReturnType<NodeWorkerSupervisorTransport["invoke"]>>,
-): Error {
-  const message = result.error?.message?.trim();
-  return new Error(message || "worker node desktop stream closed before attachment");
-}
-
 function requireLaunchReady(
   result: Awaited<ReturnType<NodeWorkerSupervisorTransport["invoke"]>>,
 ): void {
   if (!result.ok) {
-    throw invocationError(result);
+    const message = result.error?.message?.trim();
+    throw new Error(message || "worker node desktop stream closed before attachment");
   }
   let payload: unknown;
   try {
diff --git a/src/gateway/worker-environments/node-launch-adapter.ts b/src/gateway/worker-environments/node-launch-adapter.ts
index 3494d9be3616f..4c63946231108 100644
--- a/src/gateway/worker-environments/node-launch-adapter.ts
+++ b/src/gateway/worker-environments/node-launch-adapter.ts
@@ -43,24 +43,16 @@ import { WorkerRunnerCapacityError, WorkerRunnerUnavailableError } from "./tunne
 import { boundedWorkerError } from "./worker-error.js";
 
 export function nodeWorkerSpawnResultFromReceipt(
-  receipt: NodeWorkerSupervisorReceipt,
+  receipt: TerminalNodeWorkerSupervisorReceipt,
 ): SpawnResult {
-  if (
-    receipt.state === "completed" ||
-    receipt.state === "failed" ||
-    receipt.state === "interrupted" ||
-    receipt.state === "cancelled"
-  ) {
-    return {
-      stdout: receipt.state === "completed" ? receipt.resultJson : "",
-      stderr: receipt.state === "completed" ? "" : receipt.errorText,
-      code: receipt.state === "completed" ? 0 : 1,
-      signal: null,
-      killed: receipt.state === "cancelled" || receipt.state === "interrupted",
-      termination: "exit",
-    };
-  }
-  throw new Error("node worker launch returned without a terminal receipt");
+  return {
+    stdout: receipt.state === "completed" ? receipt.resultJson : "",
+    stderr: receipt.state === "completed" ? "" : receipt.errorText,
+    code: receipt.state === "completed" ? 0 : 1,
+    signal: null,
+    killed: receipt.state === "cancelled" || receipt.state === "interrupted",
+    termination: "exit",
+  };
 }
 
 const DEFAULT_RPC_TIMEOUT_MS = 30_000;

````
