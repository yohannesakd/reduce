# hyscale-lab/ARIES commit e215f33b1e

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: JooYoung Park
- Date: 2026-10-14
- Original location: https://github.com/hyscale-lab/ARIES/commit/e215f33b1e
- Copied: 2026-11-20, from the commit data and diff of the GitHub API

## Text
refactor: use native harness APIs and Gorilla WebSocket

## Diff

````diff
diff --git a/.github/configs/wordlist.txt b/.github/configs/wordlist.txt
index a942af54..f5365a1c 100644
--- a/.github/configs/wordlist.txt
+++ b/.github/configs/wordlist.txt
@@ -27,6 +27,7 @@ cpu
 cpus
 csv
 ctrf
+cwd
 deduplicates
 deepseek
 deepseek's
@@ -35,6 +36,7 @@ DNS
 docker
 Docker's
 dockerfile
+dockerfiles
 drb
 durations
 edu
@@ -50,6 +52,7 @@ gRPC
 handoff
 hermes
 hermes's
+heredocs
 hostname
 html
 http
@@ -80,6 +83,7 @@ NativeServer
 NCSpeech
 noncanonical
 nousresearch
+npm
 ntu
 nvidia
 OAuth
@@ -145,6 +149,7 @@ stdout
 stt
 subagent
 subagents
+subdirectory
 submodule
 subpackages
 substitutable
diff --git a/docs/implementation/harnesses.md b/docs/implementation/harnesses.md
index 055ec7c0..26a944a4 100644
--- a/docs/implementation/harnesses.md
+++ b/docs/implementation/harnesses.md
@@ -15,6 +15,11 @@ dispatch. `openclaw/realtime.Runner` consumes that client for talk/chat/tool
 session semantics; the gateway package intentionally contains no voice event
 parsers or Docker lifecycle.
 
+The transport uses Gorilla WebSocket for connection and frame handling, including
+legal fragmented messages and interleaved control frames. The 64 MiB limit applies
+to the assembled message; cancellation closes the connection. Gateway request
+correlation and ambiguous-admission handling remain in the existing client.
+
 Text, realtime and voice-transcribe modes share the authenticated Gateway transport. Text sends exactly one pinned-version `agent` request and correlates accepted and terminal responses by both frame request ID and non-empty run ID; an ambiguous send, disconnect, timeout, or protocol mismatch is never retried. Realtime and voice-transcribe require read and write scopes, while text requires write scope. Only sanitized role and
 sorted scope metadata may leave the authentication boundary.
 
@@ -119,6 +124,11 @@ Hermes's generic `custom` provider, which routes to `model.base_url`, in the
 rendered config. DeepSeek is a
 built-in provider and stays as written.
 
+Hermes configuration uses the repository's YAML encoder. Optional native fields
+stay omitted unless configured; explicit zero temperature remains present.
+Opaque request-body numbers retain their precision, and placeholders remain
+strings until native expansion.
+
 Fourth, three optional profile blocks render into `config.yaml` only when set:
 `model.context_length` / `max_tokens` / `temperature`, `harness.compaction`,
 and `harness.hermes.extra_body`. Compaction is a general harness capability and
diff --git a/docs/voice_mode.md b/docs/voice_mode.md
index f98aa2a5..4c9e536f 100644
--- a/docs/voice_mode.md
+++ b/docs/voice_mode.md
@@ -86,7 +86,7 @@ Use:
 }
 ```
 
-This mode follows Hermes’ voice interaction pipeline. The synthesized audio is passed as a complete utterance to the configured Hermes ASR engine for transcription. The resulting transcript is then used as input to a Hermes agent run.
+This mode follows Hermes’ voice interaction pipeline. The synthesized audio is passed as a complete utterance to the configured Hermes ASR engine for transcription. The resulting transcript is then used as input to a Hermes agent run. ARIES calls the pinned `transcribe_recording(wav_path, model=None)` API directly and retains its dictionary result. Hermes configuration selects the provider and local language; native hallucination filtering remains active.
 
 **Timeout semantics:** `harness.voice_transcribe.stt.timeout` bounds only the speech-to-text step: the time ARIES waits for Hermes to transcribe the synthesized audio before starting the agent. It does not limit the later agent run; that is still controlled by the task/harness agent timeout. This matches OpenClaw `voice-transcribe` semantics: speech recognition and agent execution have separate budgets.
 
diff --git a/go.mod b/go.mod
index 7c287361..7c33e55f 100644
--- a/go.mod
+++ b/go.mod
@@ -6,6 +6,7 @@ require (
 	github.com/BurntSushi/toml v1.6.0
 	github.com/containerd/errdefs v1.0.0
 	github.com/distribution/reference v0.6.0
+	github.com/gorilla/websocket v1.5.3
 	github.com/moby/moby/api v1.56.0
 	github.com/moby/moby/client v0.6.0
 	github.com/opencontainers/go-digest v1.0.0
diff --git a/go.sum b/go.sum
index 1a287db1..efc9f1f2 100644
--- a/go.sum
+++ b/go.sum
@@ -35,6 +35,8 @@ github.com/google/go-cmp v0.7.0 h1:wk8382ETsv4JYUZwIsn6YpYiWiBsYLSJiTsyBybVuN8=
 github.com/google/go-cmp v0.7.0/go.mod h1:pXiqmnSA92OHEEa9HXL2W4E7lf9JzCmGVUdgjX3N/iU=
 github.com/google/uuid v1.6.0 h1:NIvaJDMOsjHA8n1jAhLSgzrAzy1Hgr+hNrb57e+94F0=
 github.com/google/uuid v1.6.0/go.mod h1:TIyPZe4MgqvfeYDBFedMoGGpEw/LqOeaOT+nhxU+yHo=
+github.com/gorilla/websocket v1.5.3 h1:saDtZ6Pbx/0u+bgYQ3q96pZgCzfhKXGPqt7kZ72aNNg=
+github.com/gorilla/websocket v1.5.3/go.mod h1:YR8l580nyteQvAITg2hZ9XVh4b55+EU/adAjf1fMHhE=
 github.com/hexops/gotextdiff v1.0.3 h1:gitA9+qJrrTCsiCl7+kh75nPqQt1cx4ZkudSTLoUqJM=
 github.com/hexops/gotextdiff v1.0.3/go.mod h1:pSWU5MAI3yDq+fZBTazCSJysOMbxWL1BSow5/V2vxeg=
 github.com/klauspost/compress v1.17.9 h1:6KIumPrER1LHsvBVuDa0r5xaG0Es51mhhB9BQB2qeMA=
diff --git a/pkg/harness/hermes/config.go b/pkg/harness/hermes/config.go
index cd285858..d7b670b5 100644
--- a/pkg/harness/hermes/config.go
+++ b/pkg/harness/hermes/config.go
@@ -5,16 +5,16 @@ import (
 	"encoding/json"
 	"errors"
 	"fmt"
+	"io"
 	"math"
 	"net"
-	"sort"
 	"strconv"
 	"strings"
-	"unicode"
 
 	"github.com/hyscale-lab/aries/pkg/core"
 	"github.com/hyscale-lab/aries/pkg/harness"
 	modelconfig "github.com/hyscale-lab/aries/pkg/model"
+	"go.yaml.in/yaml/v3"
 )
 
 const (
@@ -84,8 +84,8 @@ var sandboxToolsets = []string{"terminal", "file", "code_execution"}
 // the sandbox's workdir, which comes from the bridge's endpoint rather than the
 // profile; the SSH target itself is supplied through containerEnvironment.
 //
-// Optional blocks are written only when the profile set them, so a profile
-// without them renders the same file as before they existed:
+// Optional blocks are written only when the profile sets them, preserving
+// native omission and default semantics:
 //
 //   - model.context_length and model.max_tokens feed Hermes's compressor
 //     window arithmetic and output budget. Temperature is merged into the
@@ -132,8 +132,7 @@ func renderConfig(model core.ModelConfig, settings renderSettings, voiceSTT *Voi
 			return nil, errors.New("Hermes compaction threshold must be smaller than the context length")
 		}
 	}
-	requestBody := settings.extraBody
-	if len(requestBody) != 0 && model.Provider == "deepseek" {
+	if len(settings.extraBody) != 0 && model.Provider == "deepseek" {
 		return nil, errors.New("Hermes merges user extra_body only for the custom provider, not deepseek")
 	}
 	provider := hermesProvider(model.Provider)
@@ -141,28 +140,25 @@ func renderConfig(model core.ModelConfig, settings renderSettings, voiceSTT *Voi
 	if err != nil {
 		return nil, err
 	}
-	if reasoningBody != nil {
-		object := make(map[string]json.RawMessage)
-		if len(requestBody) != 0 {
-			if err := json.Unmarshal(requestBody, &object); err != nil || len(object) == 0 {
-				return nil, errors.New("Hermes extra_body must be a non-empty JSON object")
-			}
+	requestBody := make(map[string]any)
+	if len(settings.extraBody) != 0 {
+		decoder := json.NewDecoder(bytes.NewReader(settings.extraBody))
+		decoder.UseNumber()
+		if err := decoder.Decode(&requestBody); err != nil || len(requestBody) == 0 {
+			return nil, errors.New("Hermes extra_body must be a non-empty JSON object")
+		}
+		if err := decoder.Decode(new(any)); err != io.EOF {
+			return nil, errors.New("Hermes extra_body must be a non-empty JSON object")
 		}
+	}
+	if reasoningBody != nil {
 		for _, key := range []string{"reasoning_effort", "thinking", "reasoning"} {
-			if _, exists := object[key]; exists {
+			if _, exists := requestBody[key]; exists {
 				return nil, fmt.Errorf("Hermes model.reasoning_effort conflicts with extra_body.%s", key)
 			}
 		}
 		for key, value := range reasoningBody {
-			content, err := json.Marshal(value)
-			if err != nil {
-				return nil, fmt.Errorf("Hermes reasoning request body: %w", err)
-			}
-			object[key] = content
-		}
-		requestBody, err = json.Marshal(object)
-		if err != nil {
-			return nil, fmt.Errorf("Hermes reasoning request body: %w", err)
+			requestBody[key] = value
 		}
 		// The pin's DeepSeek profile omits thinking controls for deepseek-flash.
 		// Native custom-provider extras preserve the exact requested wire fields.
@@ -172,112 +168,88 @@ func renderConfig(model core.ModelConfig, settings renderSettings, voiceSTT *Voi
 		if !harness.OpenAICompatible(model.Provider) {
 			return nil, errors.New("Hermes temperature requires the sglang or openai backend")
 		}
-		object := make(map[string]json.RawMessage)
-		if len(requestBody) != 0 {
-			if err := json.Unmarshal(requestBody, &object); err != nil || len(object) == 0 {
-				return nil, errors.New("Hermes extra_body must be a non-empty JSON object")
-			}
-		}
-		if _, exists := object["temperature"]; exists {
+		if _, exists := requestBody["temperature"]; exists {
 			return nil, errors.New("Hermes model.temperature conflicts with extra_body.temperature")
 		}
-		object["temperature"] = json.RawMessage(yamlFloat(*model.Temperature))
-		var err error
-		requestBody, err = json.Marshal(object)
-		if err != nil {
-			return nil, fmt.Errorf("Hermes request body: %w", err)
+		// The explicit tag keeps a whole temperature, including zero, a float
+		// when Hermes reads it with PyYAML.
+		requestBody["temperature"] = &yaml.Node{
+			Kind: yaml.ScalarNode, Tag: "!!float", Style: yaml.TaggedStyle,
+			Value: strconv.FormatFloat(*model.Temperature, 'g', -1, 64),
 		}
 	}
-	var extraBody string
-	if len(requestBody) != 0 {
-		if provider != "custom" {
-			return nil, errors.New("Hermes merges extra_body only for the custom provider, not " + model.Provider)
-		}
-		indented, err := indentedJSONObject(requestBody, "      ")
-		if err != nil {
-			return nil, fmt.Errorf("Hermes extra_body: %w", err)
-		}
-		extraBody = indented
-	}
-	var output bytes.Buffer
-	output.WriteString("model:\n")
-	output.WriteString("  default: " + yamlString(model.Model) + "\n")
-	output.WriteString("  provider: " + yamlString(provider) + "\n")
-	output.WriteString("  base_url: " + yamlString(model.BaseURL) + "\n")
-	output.WriteString("  api_key: " + yamlString("${"+model.APIKeyEnv+"}") + "\n")
-	output.WriteString("  api_mode: \"chat_completions\"\n")
+	modelConfig := map[string]any{
+		"default":  model.Model,
+		"provider": provider,
+		"base_url": model.BaseURL,
+		"api_key":  "${" + model.APIKeyEnv + "}",
+		"api_mode": "chat_completions",
+	}
 	if model.ContextLength > 0 {
-		output.WriteString("  context_length: " + strconv.Itoa(model.ContextLength) + "\n")
+		modelConfig["context_length"] = model.ContextLength
 	}
 	if model.MaxTokens > 0 {
-		output.WriteString("  max_tokens: " + strconv.Itoa(model.MaxTokens) + "\n")
+		modelConfig["max_tokens"] = model.MaxTokens
 	}
-	output.WriteString("\nagent:\n")
-	output.WriteString("  max_turns: " + strconv.Itoa(settings.maxTurns) + "\n")
+	agentConfig := map[string]any{"max_turns": settings.maxTurns}
 	var disabled []string
 	if !settings.subagentsEnabled {
 		disabled = append(disabled, "delegation")
 	}
 	if settings.noSandboxTools {
-		// Left out of platform_toolsets below as well; naming them here too
-		// keeps them off whatever a toolset's own default is.
+		// Keep these off whatever a toolset's own default is, as well as
+		// leaving them out of platform_toolsets below.
 		disabled = append(disabled, sandboxToolsets...)
 	}
 	if len(disabled) > 0 {
-		// The native API resolves this nested denylist after platform toolsets.
-		output.WriteString("  disabled_toolsets:\n")
-		for _, toolset := range disabled {
-			output.WriteString("    - " + toolset + "\n")
-		}
+		agentConfig["disabled_toolsets"] = disabled
+	}
+	config := map[string]any{
+		"model": modelConfig,
+		"agent": agentConfig,
+		// Listed plugins supply the per-call timing absent from the native
+		// session store. Images without hermes_otel skip the name.
+		"plugins": map[string]any{"enabled": []string{otelPluginName}},
+		"display": map[string]any{"streaming": false, "compact": true},
 	}
 	if settings.compaction != nil {
-		output.WriteString("\ncompression:\n")
+		compression := make(map[string]any)
 		if settings.compaction.Enabled != nil {
-			output.WriteString("  enabled: " + strconv.FormatBool(*settings.compaction.Enabled) + "\n")
+			compression["enabled"] = *settings.compaction.Enabled
 		}
 		if settings.compaction.ThresholdTokens > 0 {
-			output.WriteString("  threshold_tokens: " + strconv.Itoa(settings.compaction.ThresholdTokens) + "\n")
+			compression["threshold_tokens"] = settings.compaction.ThresholdTokens
+		}
+		if len(compression) == 0 {
+			config["compression"] = nil
+		} else {
+			config["compression"] = compression
 		}
 	}
-	if extraBody != "" {
-		// One entry, matched by base_url only (no model key), so it acts as
-		// the base_url fallback in Hermes's lookup and never shadows the
-		// credential or route already set in the model block above. YAML is
-		// a superset of JSON, so the object is written as an indented JSON
-		// flow mapping; Hermes then expands the ${ARIES_*} references inside
-		// it from the container environment (see containerEnvironment).
-		output.WriteString("\ncustom_providers:\n")
-		output.WriteString("  - name: \"aries\"\n")
-		output.WriteString("    base_url: " + yamlString(model.BaseURL) + "\n")
-		output.WriteString("    extra_body: " + extraBody + "\n")
+	if len(requestBody) > 0 {
+		if provider != "custom" {
+			return nil, errors.New("Hermes merges extra_body only for the custom provider, not " + model.Provider)
+		}
+		// The base_url fallback adds native request overrides without
+		// shadowing the model route or credential. Hermes expands any
+		// registered ${NAME} placeholders from its process environment.
+		config["custom_providers"] = []map[string]any{{
+			"name": "aries", "base_url": model.BaseURL,
+			"extra_body": yamlJSONNumbers(requestBody),
+		}}
 	}
 	if settings.subagentsEnabled && settings.maxConcurrentSubagents > 0 {
-		output.WriteString("\ndelegation:\n")
-		output.WriteString("  max_concurrent_children: " + strconv.Itoa(settings.maxConcurrentSubagents) + "\n")
-	}
-	// hermes_otel records each tool call, model call, and API request as a
-	// span stamped when it starts and ends. Hermes's own session store stamps
-	// messages when it saves the transcript on exit, so these spans are the
-	// only per-call timing. Hermes loads only listed plugins; an image
-	// without this one skips the name.
-	output.WriteString("\nplugins:\n")
-	output.WriteString("  enabled:\n")
-	output.WriteString("    - " + otelPluginName + "\n")
+		config["delegation"] = map[string]any{"max_concurrent_children": settings.maxConcurrentSubagents}
+	}
 	if voiceSTT != nil {
-		output.WriteString("\nstt:\n")
-		output.WriteString("  enabled: true\n")
-		output.WriteString("  provider: " + yamlString(voiceSTT.Provider) + "\n")
-		output.WriteString("  openai:\n")
-		output.WriteString("    model: " + yamlString(voiceSTT.Model) + "\n")
-		output.WriteString("  local:\n")
-		output.WriteString("    model: " + yamlString(voiceSTT.Model) + "\n")
-		output.WriteString("    language: " + yamlString(voiceSTT.Language) + "\n")
-	}
-	output.WriteString("\ndisplay:\n")
-	output.WriteString("  streaming: false\n")
-	output.WriteString("  compact: true\n")
-	// Native API agent construction resolves this platform-specific toolset list.
-	var toolsets []string
+		config["stt"] = map[string]any{
+			"enabled": true, "provider": voiceSTT.Provider,
+			"openai": map[string]any{"model": voiceSTT.Model},
+			"local":  map[string]any{"model": voiceSTT.Model, "language": voiceSTT.Language},
+		}
+	}
+	// Native API agent construction resolves this platform-specific list.
+	toolsets := []string{}
 	if !settings.noSandboxTools {
 		toolsets = append(toolsets, sandboxToolsets...)
 	}
@@ -287,76 +259,52 @@ func renderConfig(model core.ModelConfig, settings renderSettings, voiceSTT *Voi
 	if settings.webSearchEnabled {
 		toolsets = append(toolsets, "web")
 	}
-	output.WriteString("\nplatform_toolsets:\n")
-	if len(toolsets) == 0 {
-		// An explicit empty list: the agent's only tools are its MCP servers'.
-		output.WriteString("  api_server: []\n")
-	} else {
-		output.WriteString("  api_server:\n")
-		for _, toolset := range toolsets {
-			output.WriteString("    - " + toolset + "\n")
-		}
-	}
+	config["platform_toolsets"] = map[string]any{"api_server": toolsets}
 	if settings.webSearchEnabled {
-		// search_backend (not backend) is deliberate: the DRB task sandbox's
-		// SearXNG instance is search-only. extract_backend is only added when
-		// a Tavily key is staged (extractEnabled); otherwise a web_extract
-		// call fails with Hermes's own explicit "no extract backend" error
-		// rather than an ambiguous one.
-		output.WriteString("\nweb:\n")
-		output.WriteString("  search_backend: \"searxng\"\n")
+		// The sandbox's SearXNG service is search-only. Only select Tavily
+		// extraction when its private credential file is staged.
+		web := map[string]any{"search_backend": "searxng"}
 		if settings.extractEnabled {
-			output.WriteString("  extract_backend: \"tavily\"\n")
+			web["extract_backend"] = "tavily"
 		}
+		config["web"] = web
 	}
-	// Hermes registers every tool a server lists -- directly as
-	// mcp_<name>_<tool> up to v2026.8.3, and as mcp__<name>__<tool> behind
-	// its tool_describe/tool_call pair from v2026.8.31; with no MCP server
-	// named in platform_toolsets, all configured servers are enabled
-	// (hermes_cli/tools_config.py).
+	// With no MCP server named in platform_toolsets, Hermes enables all
+	// configured servers through its native tool_describe/tool_call pair.
 	if len(settings.mcpServers) > 0 {
-		output.WriteString("\nmcp_servers:\n")
+		servers := make(map[string]any, len(settings.mcpServers))
 		for _, server := range settings.mcpServers {
-			output.WriteString("  " + server.Name + ":\n")
+			entry := make(map[string]any)
 			if server.URL != "" {
-				output.WriteString("    url: " + yamlString(server.URL) + "\n")
-				// streamable-http is Hermes's default when the key is absent.
+				entry["url"] = server.URL
+				// streamable-http is Hermes's default when this key is absent.
 				if server.Transport == "sse" {
-					output.WriteString("    transport: \"sse\"\n")
+					entry["transport"] = "sse"
 				}
 			} else if server.Command != "" {
-				output.WriteString("    command: " + yamlString(server.Command) + "\n")
+				entry["command"] = server.Command
 				if len(server.Args) > 0 {
-					output.WriteString("    args:\n")
-					for _, arg := range server.Args {
-						output.WriteString("      - " + yamlString(arg) + "\n")
-					}
+					entry["args"] = server.Args
 				}
 				if len(server.Env) > 0 || len(server.SecretEnv) > 0 {
-					output.WriteString("    env:\n")
-					keys := make([]string, 0, len(server.Env)+len(server.SecretEnv))
-					for k := range server.Env {
-						keys = append(keys, k)
-					}
-					for k := range server.SecretEnv {
-						keys = append(keys, k)
+					environment := make(map[string]string, len(server.Env)+len(server.SecretEnv))
+					for key, value := range server.Env {
+						environment[key] = value
 					}
-					sort.Strings(keys)
-					for _, k := range keys {
-						if hostVar, ok := server.SecretEnv[k]; ok {
-							output.WriteString("      " + k + ": " + yamlString("${"+hostVar+"}") + "\n")
-						} else {
-							output.WriteString("      " + k + ": " + yamlString(server.Env[k]) + "\n")
-						}
+					for key, hostVar := range server.SecretEnv {
+						environment[key] = "${" + hostVar + "}"
 					}
+					entry["env"] = environment
 				}
 			}
 			if server.TimeoutSeconds > 0 {
-				output.WriteString("    timeout: " + strconv.Itoa(server.TimeoutSeconds) + "\n")
+				entry["timeout"] = server.TimeoutSeconds
 			}
+			servers[server.Name] = entry
 		}
+		config["mcp_servers"] = servers
 	}
-	return output.Bytes(), nil
+	return yaml.Marshal(config)
 }
 
 // renderTerminal is the `terminal:` section appended to config.yaml. Hermes
@@ -376,12 +324,10 @@ func renderTerminal(workdir string, timeout int) ([]byte, error) {
 	if timeout <= 0 {
 		return nil, errors.New("Hermes terminal timeout must be positive")
 	}
-	var output bytes.Buffer
-	output.WriteString("\nterminal:\n")
-	output.WriteString("  backend: \"ssh\"\n")
-	output.WriteString("  cwd: " + yamlString(workdir) + "\n")
-	output.WriteString("  timeout: " + strconv.Itoa(timeout) + "\n")
-	return output.Bytes(), nil
+	rendered, err := yaml.Marshal(map[string]any{
+		"terminal": map[string]any{"backend": "ssh", "cwd": workdir, "timeout": timeout},
+	})
+	return append([]byte("\n"), rendered...), err
 }
 
 // validateGeneration mirrors pkg/config's checks so a caller that bypasses the
@@ -402,30 +348,27 @@ func validateGeneration(model core.ModelConfig) error {
 	return nil
 }
 
-// indentedJSONObject checks that raw is a non-empty JSON object and re-indents
-// it so every continuation line sits under the YAML key that owns it. The
-// bytes are re-indented, not re-encoded, so key order and number lexemes stay
-// exactly as the profile wrote them.
-func indentedJSONObject(raw []byte, prefix string) (string, error) {
-	var object map[string]json.RawMessage
-	if err := json.Unmarshal(raw, &object); err != nil || len(object) == 0 {
-		return "", errors.New("must be a non-empty JSON object")
-	}
-	var indented bytes.Buffer
-	if err := json.Indent(&indented, raw, prefix, "  "); err != nil {
-		return "", err
-	}
-	return indented.String(), nil
-}
-
-// yamlFloat writes a finite float as a YAML float scalar. A whole number keeps
-// a trailing ".0" so YAML does not read it as an integer.
-func yamlFloat(value float64) string {
-	text := strconv.FormatFloat(value, 'f', -1, 64)
-	if !strings.ContainsAny(text, ".eE") {
-		text += ".0"
-	}
-	return text
+// yamlJSONNumbers preserves JSON number precision in the request-body subtree.
+// Explicit float tags also make exponent-only literals numeric in Hermes's
+// YAML 1.1 reader; decoding through float64 would round large integers first.
+func yamlJSONNumbers(value any) any {
+	switch value := value.(type) {
+	case json.Number:
+		node := &yaml.Node{Kind: yaml.ScalarNode, Tag: "!!int", Value: value.String()}
+		if strings.ContainsAny(value.String(), ".eE") {
+			node.Tag, node.Style = "!!float", yaml.TaggedStyle
+		}
+		return node
+	case map[string]any:
+		for key, child := range value {
+			value[key] = yamlJSONNumbers(child)
+		}
+	case []any:
+		for index, child := range value {
+			value[index] = yamlJSONNumbers(child)
+		}
+	}
+	return value
 }
 
 // containerEnvironment is the non-secret environment given to the Hermes
@@ -589,38 +532,3 @@ func validWorkdir(value string) bool {
 	}
 	return true
 }
-
-// yamlString emits a double-quoted YAML scalar. Every character that could
-// terminate the scalar or be read as a line break is escaped, so no rendered
-// value can restructure the document: the quote and backslash, the three
-// whitespace controls with short forms, and any remaining control character or
-// Unicode line/paragraph separator as a numeric escape.
-func yamlString(value string) string {
-	var output strings.Builder
-	output.WriteByte('"')
-	for _, character := range value {
-		switch {
-		case character == '"':
-			output.WriteString(`\"`)
-		case character == '\\':
-			output.WriteString(`\\`)
-		case character == '\n':
-			output.WriteString(`\n`)
-		case character == '\r':
-			output.WriteString(`\r`)
-		case character == '\t':
-			output.WriteString(`\t`)
-		case character == '\u2028':
-			output.WriteString(`\L`)
-		case character == '\u2029':
-			output.WriteString(`\P`)
-		case unicode.IsControl(character):
-			// IsControl covers C0, DEL, and C1; all fit the two-digit form.
-			fmt.Fprintf(&output, `\x%02X`, character)
-		default:
-			output.WriteRune(character)
-		}
-	}
-	output.WriteByte('"')
-	return output.String()
-}
diff --git a/pkg/harness/hermes/config_context_test.go b/pkg/harness/hermes/config_context_test.go
index af396b04..38347924 100644
--- a/pkg/harness/hermes/config_context_test.go
+++ b/pkg/harness/hermes/config_context_test.go
@@ -41,10 +41,11 @@ func TestRenderConfigEmitsGenerationSettingsOnlyWhenSet(t *testing.T) {
 	model := vllmModel()
 	model.ContextLength, model.MaxTokens, model.Temperature = 262144, 32768, floatPtr(1)
 	text := mustRender(t, model, baseSettings())
-	for _, line := range []string{"  context_length: 262144\n", "  max_tokens: 32768\n", `"temperature": 1.0`} {
-		if !strings.Contains(text, line) {
-			t.Fatalf("missing %q:\n%s", line, text)
-		}
+	config := decodeConfigYAML(t, []byte(text))
+	nativeModel := config["model"].(map[string]any)
+	body := config["custom_providers"].([]any)[0].(map[string]any)["extra_body"].(map[string]any)
+	if nativeModel["context_length"] != 262144 || nativeModel["max_tokens"] != 32768 || body["temperature"] != float64(1) {
+		t.Fatalf("generation settings = %#v / %#v", nativeModel, body)
 	}
 	bad := map[string]func(*core.ModelConfig){
 		"max tokens fills window": func(m *core.ModelConfig) { m.ContextLength, m.MaxTokens = 1000, 1000 },
@@ -75,12 +76,18 @@ func TestRenderConfigEmitsCompactionBlockOnlyWhenSet(t *testing.T) {
 		t.Fatal(err)
 	}
 	_, hasEnabled := parsed.Compression["enabled"]
-	if !strings.Contains(text, "\ncompression:\n  threshold_tokens: 65536\n") || hasEnabled {
+	if parsed.Compression["threshold_tokens"] != 65536 || hasEnabled {
 		t.Fatalf("threshold-only compaction block is wrong:\n%s", text)
 	}
 	settings.compaction = &CompactionSettings{Enabled: boolPtr(false)}
-	if !strings.Contains(mustRender(t, vllmModel(), settings), "\ncompression:\n  enabled: false\n") {
-		t.Fatal("disabled compaction was not rendered")
+	disabled := decodeConfigYAML(t, []byte(mustRender(t, vllmModel(), settings)))["compression"].(map[string]any)
+	if disabled["enabled"] != false || len(disabled) != 1 {
+		t.Fatalf("disabled compaction = %#v", disabled)
+	}
+	settings.compaction = &CompactionSettings{}
+	empty := decodeConfigYAML(t, []byte(mustRender(t, vllmModel(), settings)))
+	if value, exists := empty["compression"]; !exists || value != nil {
+		t.Fatalf("empty compaction = %#v", empty)
 	}
 	model := vllmModel()
 	model.ContextLength = 65536
@@ -94,8 +101,7 @@ func TestRenderConfigEmitsCompactionBlockOnlyWhenSet(t *testing.T) {
 	}
 }
 
-// The profile's extra_body is written verbatim as an indented JSON flow
-// mapping. A YAML reader must recover the same object, with the ${ARIES_*}
+// A YAML reader must recover the opaque JSON object, with the ${ARIES_*}
 // references left for Hermes to expand.
 func TestRenderConfigWritesExtraBodyAsYAMLReadableJSON(t *testing.T) {
 	if strings.Contains(mustRender(t, vllmModel(), baseSettings()), "custom_providers:") {
@@ -131,10 +137,10 @@ func TestRenderConfigWritesExtraBodyAsYAMLReadableJSON(t *testing.T) {
 		t.Fatalf("metadata = %#v", meta)
 	}
 	odd, _ := entry.ExtraBody["odd"].([]any)
-	if len(odd) != 7 || odd[0] != "a: b" || odd[1] != "x<y #z" || odd[2] != nil || odd[4] != "tab\tchar" || odd[5] != `q"q` || odd[6] != "brace }" {
+	if len(odd) != 7 || odd[0] != "a: b" || odd[1] != "x<y #z" || odd[2] != nil || odd[3] != float64(1000) || odd[4] != "tab\tchar" || odd[5] != `q"q` || odd[6] != "brace }" {
 		t.Fatalf("odd = %#v", odd)
 	}
-	for _, bad := range []string{`[1]`, `"x"`, `{}`, `null`, `{"a":`, ``} {
+	for _, bad := range []string{`[1]`, `"x"`, `{}`, `null`, `{"a":`, `{"a":1} {"b":2}`, `{"a":1} trailing`, ``} {
 		settings.extraBody = []byte(bad)
 		if _, err := renderConfig(vllmModel(), settings, nil); err == nil && bad != "" {
 			t.Fatalf("accepted extra_body %q", bad)
@@ -183,11 +189,11 @@ func TestStartRendersContextBlocksAndExportsIDs(t *testing.T) {
 	if err != nil {
 		t.Fatal(err)
 	}
-	text := string(retained)
-	for _, line := range []string{`"user": "${ARIES_RUN_ID}-${ARIES_TASK_ID}"`, `provider: "custom"`, "threshold_tokens: 65536", "context_length: 262144", `${VLLM_API_KEY}`} {
-		if !strings.Contains(text, line) {
-			t.Fatalf("retained config lacks %q:\n%s", line, text)
-		}
+	config := decodeConfigYAML(t, retained)
+	nativeModel := config["model"].(map[string]any)
+	body := config["custom_providers"].([]any)[0].(map[string]any)["extra_body"].(map[string]any)
+	if nativeModel["provider"] != "custom" || nativeModel["api_key"] != "${VLLM_API_KEY}" || nativeModel["context_length"] != 262144 || config["compression"].(map[string]any)["threshold_tokens"] != 65536 || body["user"] != "${ARIES_RUN_ID}-${ARIES_TASK_ID}" {
+		t.Fatalf("retained config = %#v", config)
 	}
 	joined := strings.Join(fake.created.Env, "\n")
 	for _, want := range []string{"ARIES_RUN_ID=run-7", "ARIES_TASK_ID=fix-git"} {
@@ -237,6 +243,43 @@ func TestRenderTemperatureUsesRequestExtraBody(t *testing.T) {
 	}
 }
 
+func TestRenderConfigPreservesJSONNumericPrecision(t *testing.T) {
+	settings := baseSettings()
+	settings.extraBody = []byte(`{"integer":9007199254740993,"huge":18446744073709551617,"decimal":0.1234567890123456789012345,"scientific":1e3,"nested":[0.0,"1e3"]}`)
+	text := mustRender(t, vllmModel(), settings)
+	var parsed struct {
+		Providers []struct {
+			Body yaml.Node `yaml:"extra_body"`
+		} `yaml:"custom_providers"`
+	}
+	if err := yaml.Unmarshal([]byte(text), &parsed); err != nil {
+		t.Fatal(err)
+	}
+	body := parsed.Providers[0].Body
+	want := map[string][2]string{
+		"integer":    {"!!int", "9007199254740993"},
+		"huge":       {"!!int", "18446744073709551617"},
+		"decimal":    {"!!float", "0.1234567890123456789012345"},
+		"scientific": {"!!float", "1e3"},
+	}
+	for index := 0; index < len(body.Content); index += 2 {
+		key, value := body.Content[index].Value, body.Content[index+1]
+		if key == "nested" {
+			if len(value.Content) != 2 || value.Content[0].Tag != "!!float" || value.Content[0].Value != "0.0" || value.Content[1].Tag != "!!str" || value.Content[1].Value != "1e3" {
+				t.Fatalf("nested numbers changed: %#v", value.Content)
+			}
+			continue
+		}
+		if got := [2]string{value.Tag, value.Value}; got != want[key] {
+			t.Fatalf("%s = %#v, want %#v", key, got, want[key])
+		}
+		delete(want, key)
+	}
+	if len(want) != 0 {
+		t.Fatalf("request numbers omitted: %#v", want)
+	}
+}
+
 func TestRenderReasoningUsesNativeRequestOverrides(t *testing.T) {
 	for _, test := range []struct {
 		provider, model, effort, wireEffort, thinking string
diff --git a/pkg/harness/hermes/config_gateway_test.go b/pkg/harness/hermes/config_gateway_test.go
index c25967c7..b820b043 100644
--- a/pkg/harness/hermes/config_gateway_test.go
+++ b/pkg/harness/hermes/config_gateway_test.go
@@ -3,9 +3,12 @@ package hermes
 import (
 	"context"
 	"errors"
-	"github.com/hyscale-lab/aries/pkg/core"
+	"reflect"
+	"slices"
 	"strings"
 	"testing"
+
+	"github.com/hyscale-lab/aries/pkg/core"
 )
 
 func TestGatewayConfigPreservesNativeDefaultsAndExplicitDelegationPolicy(t *testing.T) {
@@ -18,8 +21,9 @@ func TestGatewayConfigPreservesNativeDefaultsAndExplicitDelegationPolicy(t *test
 			t.Errorf("overrode native default %q", section)
 		}
 	}
-	if !strings.Contains(string(rendered), "\nagent:\n  max_turns: 10\n  disabled_toolsets:\n    - delegation\n") {
-		t.Fatal("missing explicit delegation policy")
+	config := decodeConfigYAML(t, rendered)
+	if !reflect.DeepEqual(config["agent"], map[string]any{"max_turns": 10, "disabled_toolsets": []any{"delegation"}}) {
+		t.Fatalf("agent settings = %#v", config["agent"])
 	}
 	if strings.Contains(string(rendered), "\ndisabled_toolsets:") {
 		t.Fatal("API ignores top-level disabled_toolsets")
@@ -32,8 +36,9 @@ func TestGatewayConfigExplicitlyEnablesDelegation(t *testing.T) {
 		t.Fatal(err)
 	}
 	text := string(rendered)
-	if !strings.Contains(text, "    - delegation\n") || !strings.Contains(text, "\ndelegation:\n  max_concurrent_children: 2\n") {
-		t.Fatal("delegation not enabled and bounded")
+	config := decodeConfigYAML(t, rendered)
+	if !slices.Contains(config["platform_toolsets"].(map[string]any)["api_server"].([]any), any("delegation")) || config["delegation"].(map[string]any)["max_concurrent_children"] != 2 {
+		t.Fatalf("delegation settings = %#v", config)
 	}
 	if strings.Contains(text, "disabled_toolsets:") {
 		t.Fatal("enabled delegation has denylist")
@@ -71,7 +76,9 @@ func TestGatewayAllowsReservedMCPChildAlias(t *testing.T) {
 	if err != nil {
 		t.Fatal(err)
 	}
-	if !strings.Contains(string(rendered), `API_SERVER_KEY: "${SERVICE_TOKEN}"`) {
+	config := decodeConfigYAML(t, rendered)
+	service := config["mcp_servers"].(map[string]any)["service"].(map[string]any)
+	if service["env"].(map[string]any)["API_SERVER_KEY"] != "${SERVICE_TOKEN}" {
 		t.Fatal("MCP child alias was not preserved")
 	}
 }
diff --git a/pkg/harness/hermes/config_test.go b/pkg/harness/hermes/config_test.go
index aeccc65c..43c9a61c 100644
--- a/pkg/harness/hermes/config_test.go
+++ b/pkg/harness/hermes/config_test.go
@@ -1,10 +1,14 @@
 package hermes
 
 import (
+	"encoding/json"
+	"reflect"
+	"slices"
 	"strings"
 	"testing"
 
 	"github.com/hyscale-lab/aries/pkg/core"
+	"go.yaml.in/yaml/v3"
 )
 
 func validModel() core.ModelConfig {
@@ -22,9 +26,10 @@ func TestRenderTerminalNamesTheSandboxWorkdir(t *testing.T) {
 	if err != nil {
 		t.Fatal(err)
 	}
-	want := "\nterminal:\n  backend: \"ssh\"\n  cwd: \"/workspace/dumps/workspace\"\n  timeout: 180\n"
-	if string(rendered) != want {
-		t.Fatalf("terminal section = %q, want %q", rendered, want)
+	terminal := decodeConfigYAML(t, rendered)["terminal"]
+	want := map[string]any{"backend": "ssh", "cwd": "/workspace/dumps/workspace", "timeout": 180}
+	if !reflect.DeepEqual(terminal, want) {
+		t.Fatalf("terminal = %#v, want %#v", terminal, want)
 	}
 	for _, workdir := range []string{"", "relative", "/app/", "/a b", "/a/../b", "/a;b"} {
 		if _, err := renderTerminal(workdir, 180); err == nil {
@@ -39,22 +44,22 @@ func TestRenderTerminalNamesTheSandboxWorkdir(t *testing.T) {
 // The credential must reach the container as a ${NAME} reference that Hermes
 // expands at run time, never as a value written into the rendered config.
 func TestRenderConfigReferencesCredentialByName(t *testing.T) {
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 90, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 0}, nil)
-
+	rendered, err := renderConfig(validModel(), baseSettings(), nil)
 	if err != nil {
 		t.Fatal(err)
 	}
-	text := string(rendered)
-	if !strings.Contains(text, `api_key: "${DEEPSEEK_API_KEY}"`) {
-		t.Fatalf("config does not reference the credential by name:\n%s", text)
+	config := decodeConfigYAML(t, rendered)
+	model := config["model"].(map[string]any)
+	if model["api_key"] != "${DEEPSEEK_API_KEY}" {
+		t.Fatalf("credential reference = %#v", model)
 	}
 	for _, forbidden := range []string{"sk-", "terminal:", "backend:"} {
-		if strings.Contains(text, forbidden) {
-			t.Fatalf("config unexpectedly contains %q:\n%s", forbidden, text)
+		if strings.Contains(string(rendered), forbidden) {
+			t.Fatalf("config unexpectedly contains %q:\n%s", forbidden, rendered)
 		}
 	}
-	if !strings.Contains(text, "max_turns: 90") || !strings.Contains(text, "- terminal") {
-		t.Fatalf("config is missing agent or toolset settings:\n%s", text)
+	if config["agent"].(map[string]any)["max_turns"] != 90 || !slices.Contains(config["platform_toolsets"].(map[string]any)["api_server"].([]any), any("terminal")) {
+		t.Fatalf("missing agent or toolset settings: %#v", config)
 	}
 }
 
@@ -67,7 +72,7 @@ func TestRenderConfigNormalizesSGLangAndRejectsBadInput(t *testing.T) {
 	if err != nil {
 		t.Fatal(err)
 	}
-	if !strings.Contains(string(rendered), `base_url: "http://host:30000/v1"`) {
+	if decodeConfigYAML(t, rendered)["model"].(map[string]any)["base_url"] != "http://host:30000/v1" {
 		t.Fatalf("SGLang base URL was not normalized:\n%s", rendered)
 	}
 	bad := map[string]func(*core.ModelConfig){
@@ -94,64 +99,49 @@ func TestRenderConfigNormalizesSGLangAndRejectsBadInput(t *testing.T) {
 func TestRenderConfigQuotesInjectionAttempts(t *testing.T) {
 	model := validModel()
 	model.Model = `x" \nevil: true`
-	rendered, err := renderConfig(model, renderSettings{maxTurns: 10, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 0}, nil)
-
+	rendered, err := renderConfig(model, baseSettings(), nil)
 	if err != nil {
 		t.Fatal(err)
 	}
-	// The model ID carries a literal backslash-n. It must reach the file as a
-	// doubled backslash, not as the `\n` escape a YAML parser would decode
-	// into a line break that starts a new key.
-	if !strings.Contains(string(rendered), `\\nevil: true`) {
-		t.Fatalf("model ID escaped its scalar:\n%s", rendered)
+	config := decodeConfigYAML(t, rendered)
+	nativeModel := config["model"].(map[string]any)
+	if nativeModel["default"] != model.Model {
+		t.Fatalf("model ID changed: %#v", nativeModel)
 	}
-	if !strings.Contains(string(rendered), `\"`) {
-		t.Fatalf("model ID quote was not escaped:\n%s", rendered)
+	if _, exists := nativeModel["evil"]; exists {
+		t.Fatal("model ID injected a field")
+	}
+	if _, exists := config["evil"]; exists {
+		t.Fatal("model ID injected a section")
 	}
 }
 
 func TestRenderConfigAddsVoiceSTTProvider(t *testing.T) {
 	voiceSTT := VoiceSTTOptions{Provider: "openai", Model: "gpt-4o-mini-transcribe", Language: "en"}
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 90, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 0}, &voiceSTT)
+	rendered, err := renderConfig(validModel(), baseSettings(), &voiceSTT)
 	if err != nil {
 		t.Fatal(err)
 	}
-	text := string(rendered)
-	for _, want := range []string{
-		"\nstt:\n",
-		"  enabled: true\n",
-		"  provider: \"openai\"\n",
-		"  openai:\n    model: \"gpt-4o-mini-transcribe\"\n",
-		"  local:\n    model: \"gpt-4o-mini-transcribe\"\n    language: \"en\"\n",
-	} {
-		if !strings.Contains(text, want) {
-			t.Fatalf("config is missing %q:\n%s", want, text)
-		}
+	want := map[string]any{
+		"enabled": true, "provider": "openai",
+		"openai": map[string]any{"model": "gpt-4o-mini-transcribe"},
+		"local":  map[string]any{"model": "gpt-4o-mini-transcribe", "language": "en"},
+	}
+	if got := decodeConfigYAML(t, rendered)["stt"]; !reflect.DeepEqual(got, want) {
+		t.Fatalf("stt = %#v, want %#v", got, want)
 	}
 }
 
-// A control byte cannot reach yamlString through renderConfig because
-// validateModel rejects it first, so the renderer is covered directly: a raw
-// control byte in a double-quoted scalar is invalid YAML, and Hermes would fail
-// to parse its own config well after the cause.
-func TestYAMLStringEscapesControlCharacters(t *testing.T) {
-	for _, test := range []struct{ name, value, want string }{
-		{"nul", "a\x00b", `"a\x00b"`},
-		{"bell", "a\x07b", `"a\x07b"`},
-		{"vertical tab", "a\x0bb", `"a\x0Bb"`},
-		{"escape", "a\x1bb", `"a\x1Bb"`},
-		{"delete", "a\x7fb", `"a\x7Fb"`},
-		{"next line", "a\u0085b", `"a\x85b"`},
-		{"line separator", "a\u2028b", `"a\Lb"`},
-		{"paragraph separator", "a\u2029b", `"a\Pb"`},
-		{"short forms retained", "a\n\r\tb", `"a\n\r\tb"`},
-		{"printable untouched", "deepseek-v4/flash_1", `"deepseek-v4/flash_1"`},
-	} {
-		t.Run(test.name, func(t *testing.T) {
-			if got := yamlString(test.value); got != test.want {
-				t.Fatalf("yamlString(%q) = %s, want %s", test.value, got, test.want)
-			}
-		})
+// Opaque JSON strings must survive the YAML boundary without restructuring it.
+func TestRenderConfigPreservesControlCharactersInExtraBody(t *testing.T) {
+	for _, value := range []string{"a\x00b", "a\x07b", "a\x0bb", "a\x1bb", "a\x7fb", "a\u0085b", "a\u2028b", "a\u2029b", "a\n\r\tb", "deepseek-v4/flash_1"} {
+		settings := baseSettings()
+		settings.extraBody, _ = json.Marshal(map[string]string{"value": value})
+		config := decodeConfigYAML(t, []byte(mustRender(t, vllmModel(), settings)))
+		body := config["custom_providers"].([]any)[0].(map[string]any)["extra_body"].(map[string]any)
+		if body["value"] != value {
+			t.Fatalf("JSON string %q changed to %#v", value, body["value"])
+		}
 	}
 }
 
@@ -212,8 +202,9 @@ func TestRenderConfigAlwaysEnablesOTelPlugin(t *testing.T) {
 	for _, subagents := range []bool{false, true} {
 		settings := baseSettings()
 		settings.subagentsEnabled = subagents
-		if text := mustRender(t, vllmModel(), settings); !strings.Contains(text, "\nplugins:\n  enabled:\n    - hermes_otel\n") {
-			t.Fatalf("config does not enable hermes_otel:\n%s", text)
+		config := decodeConfigYAML(t, []byte(mustRender(t, vllmModel(), settings)))
+		if got := config["plugins"].(map[string]any)["enabled"]; !reflect.DeepEqual(got, []any{"hermes_otel"}) {
+			t.Fatalf("enabled plugins = %#v", got)
 		}
 	}
 }
@@ -265,16 +256,11 @@ func TestRenderConfigOmitsWebToolsetWhenDisabled(t *testing.T) {
 }
 
 func TestRenderConfigAddsWebToolsetWhenEnabled(t *testing.T) {
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 90, webSearchEnabled: true, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 0}, nil)
-
-	if err != nil {
-		t.Fatal(err)
-	}
-	text := string(rendered)
-	for _, want := range []string{"    - web\n", "\nweb:\n  search_backend: \"searxng\"\n"} {
-		if !strings.Contains(text, want) {
-			t.Fatalf("config is missing %q:\n%s", want, text)
-		}
+	settings := baseSettings()
+	settings.webSearchEnabled = true
+	config := decodeConfigYAML(t, []byte(mustRender(t, validModel(), settings)))
+	if !slices.Contains(config["platform_toolsets"].(map[string]any)["api_server"].([]any), any("web")) || config["web"].(map[string]any)["search_backend"] != "searxng" {
+		t.Fatalf("web settings = %#v", config)
 	}
 }
 
@@ -293,16 +279,11 @@ func TestRenderConfigOmitsExtractBackendWithoutExtractKey(t *testing.T) {
 }
 
 func TestRenderConfigAddsExtractBackendWhenEnabled(t *testing.T) {
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 90, webSearchEnabled: true, extractEnabled: true, subagentsEnabled: true, maxConcurrentSubagents: 0}, nil)
-
-	if err != nil {
-		t.Fatal(err)
-	}
-	text := string(rendered)
-	for _, want := range []string{"    - web\n", "  search_backend: \"searxng\"\n", "  extract_backend: \"tavily\"\n"} {
-		if !strings.Contains(text, want) {
-			t.Fatalf("config is missing %q:\n%s", want, text)
-		}
+	settings := baseSettings()
+	settings.webSearchEnabled, settings.extractEnabled = true, true
+	config := decodeConfigYAML(t, []byte(mustRender(t, validModel(), settings)))
+	if !slices.Contains(config["platform_toolsets"].(map[string]any)["api_server"].([]any), any("web")) || !reflect.DeepEqual(config["web"], map[string]any{"search_backend": "searxng", "extract_backend": "tavily"}) {
+		t.Fatalf("web settings = %#v", config)
 	}
 }
 
@@ -321,14 +302,9 @@ func TestRenderConfigOmitsExtractBackendWhenWebSearchDisabled(t *testing.T) {
 }
 
 func TestRenderConfigDisablesDelegationToolsetWhenSubagentsDisabled(t *testing.T) {
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 90, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: false, maxConcurrentSubagents: 0}, nil)
-
-	if err != nil {
-		t.Fatal(err)
-	}
-	text := string(rendered)
-	if !strings.Contains(text, "\n  disabled_toolsets:\n    - delegation\n") {
-		t.Fatalf("config is missing disabled_toolsets: [delegation]:\n%s", text)
+	config := decodeConfigYAML(t, []byte(mustRender(t, validModel(), renderSettings{maxTurns: 90})))
+	if got := config["agent"].(map[string]any)["disabled_toolsets"]; !reflect.DeepEqual(got, []any{"delegation"}) {
+		t.Fatalf("disabled toolsets = %#v", got)
 	}
 }
 
@@ -345,14 +321,11 @@ func TestRenderConfigOmitsDisabledToolsetsWhenSubagentsEnabled(t *testing.T) {
 }
 
 func TestRenderConfigSetsMaxConcurrentChildrenWhenLimited(t *testing.T) {
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 90, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 2}, nil)
-
-	if err != nil {
-		t.Fatal(err)
-	}
-	text := string(rendered)
-	if !strings.Contains(text, "\ndelegation:\n  max_concurrent_children: 2\n") {
-		t.Fatalf("config is missing delegation.max_concurrent_children:\n%s", text)
+	settings := baseSettings()
+	settings.maxConcurrentSubagents = 2
+	config := decodeConfigYAML(t, []byte(mustRender(t, validModel(), settings)))
+	if got := config["delegation"]; !reflect.DeepEqual(got, map[string]any{"max_concurrent_children": 2}) {
+		t.Fatalf("delegation = %#v", got)
 	}
 }
 
@@ -444,73 +417,38 @@ func TestGatewayLauncherExportsExtractKeyWhenEnabled(t *testing.T) {
 // OpenAI-compatible backends use Hermes's "custom" provider; DeepSeek remains native.
 func TestRenderConfigMapsOpenAICompatibleBackendsToCustomProvider(t *testing.T) {
 	for _, provider := range []string{"sglang", "openai"} {
-		model := validModel()
+		model := vllmModel()
 		model.Provider = provider
-		model.BaseURL = "http://vllm.local:8000/v1"
-		rendered, err := renderConfig(model, renderSettings{maxTurns: 10, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 0}, nil)
-
-		if err != nil {
-			t.Fatal(err)
+		config := decodeConfigYAML(t, []byte(mustRender(t, model, baseSettings())))
+		if config["model"].(map[string]any)["provider"] != "custom" || hermesProvider(provider) != "custom" {
+			t.Fatalf("%s provider = %#v", provider, config["model"])
 		}
-		text := string(rendered)
-		if !strings.Contains(text, `provider: "custom"`) || strings.Contains(text, `provider: "`+provider+`"`) {
-			t.Fatalf("%s backend was not rendered as the custom provider:\n%s", provider, text)
-		}
-		if got := hermesProvider(provider); got != "custom" {
-			t.Fatalf("hermesProvider(%s) = %q", provider, got)
-		}
-	}
-	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 10, webSearchEnabled: false, extractEnabled: false, subagentsEnabled: true, maxConcurrentSubagents: 0}, nil)
-
-	if err != nil {
-		t.Fatal(err)
 	}
-	if !strings.Contains(string(rendered), `provider: "deepseek"`) || hermesProvider("deepseek") != "deepseek" {
-		t.Fatal("deepseek provider was rewritten")
+	config := decodeConfigYAML(t, []byte(mustRender(t, validModel(), baseSettings())))
+	if config["model"].(map[string]any)["provider"] != "deepseek" || hermesProvider("deepseek") != "deepseek" {
+		t.Fatal("DeepSeek provider was rewritten")
 	}
 }
 
 func TestRenderConfig_MCPServers(t *testing.T) {
 	servers := []core.MCPServerConfig{
-		{
-			Name:      "filesystem",
-			Command:   "npx",
-			Args:      []string{"-y", "@modelcontextprotocol/server-filesystem", "/workspace"},
-			Env:       map[string]string{"DEBUG": "1"},
-			SecretEnv: map[string]string{"API_KEY": "TOOLATHLON_API_KEY"},
-		},
-		{
-			Name: "remote-sse",
-			URL:  "https://mcp.example.com/sse",
-		},
-	}
-
-	rendered, err := renderConfig(validModel(), renderSettings{
-		maxTurns:   10,
-		mcpServers: servers,
-	}, nil)
-	if err != nil {
-		t.Fatalf("renderConfig failed: %v", err)
-	}
-
-	text := string(rendered)
-	if strings.Contains(text, "custom_tools") {
-		t.Fatalf("rendered config contains invalid custom_tools field:\n%s", text)
+		{Name: "filesystem", Command: "npx", Args: []string{"-y", "@modelcontextprotocol/server-filesystem", "/workspace"}, Env: map[string]string{"DEBUG": "1"}, SecretEnv: map[string]string{"API_KEY": "TOOLATHLON_API_KEY"}},
+		{Name: "remote-sse", URL: "https://mcp.example.com/sse"},
 	}
-	if !strings.Contains(text, "mcp_servers:") {
-		t.Fatalf("rendered config missing mcp_servers block:\n%s", text)
-	}
-	if !strings.Contains(text, "filesystem:") || !strings.Contains(text, `command: "npx"`) {
-		t.Fatalf("rendered config missing filesystem command:\n%s", text)
+	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 10, mcpServers: servers}, nil)
+	if err != nil {
+		t.Fatal(err)
 	}
-	if !strings.Contains(text, `- "-y"`) || !strings.Contains(text, `- "@modelcontextprotocol/server-filesystem"`) {
-		t.Fatalf("rendered config missing filesystem arguments:\n%s", text)
+	config := decodeConfigYAML(t, rendered)
+	if _, exists := config["custom_tools"]; exists {
+		t.Fatal("rendered invalid custom_tools field")
 	}
-	if !strings.Contains(text, "env:") || !strings.Contains(text, `API_KEY: "${TOOLATHLON_API_KEY}"`) || !strings.Contains(text, `DEBUG: "1"`) {
-		t.Fatalf("rendered config missing filesystem env mapping:\n%s", text)
+	want := map[string]any{
+		"filesystem": map[string]any{"command": "npx", "args": []any{"-y", "@modelcontextprotocol/server-filesystem", "/workspace"}, "env": map[string]any{"DEBUG": "1", "API_KEY": "${TOOLATHLON_API_KEY}"}},
+		"remote-sse": map[string]any{"url": "https://mcp.example.com/sse"},
 	}
-	if !strings.Contains(text, "remote-sse:") || !strings.Contains(text, `url: "https://mcp.example.com/sse"`) {
-		t.Fatalf("rendered config missing remote-sse url:\n%s", text)
+	if got := config["mcp_servers"]; !reflect.DeepEqual(got, want) {
+		t.Fatalf("MCP servers = %#v, want %#v", got, want)
 	}
 }
 
@@ -538,24 +476,19 @@ func TestSearchRequiresResolvedEndpoint(t *testing.T) {
 }
 
 func TestRenderConfig_MCPServerTransportAndTimeout(t *testing.T) {
-	rendered, err := renderConfig(validModel(), renderSettings{
-		maxTurns: 10,
-		mcpServers: []core.MCPServerConfig{
-			{Name: "gateway", URL: "http://task-sandbox:10086/sse", Transport: "sse", TimeoutSeconds: 1200},
-			{Name: "streaming", URL: "https://mcp.example.com/mcp", Transport: "streamable-http"},
-		},
-	}, nil)
+	rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 10, mcpServers: []core.MCPServerConfig{
+		{Name: "gateway", URL: "http://task-sandbox:10086/sse", Transport: "sse", TimeoutSeconds: 1200},
+		{Name: "streaming", URL: "https://mcp.example.com/mcp", Transport: "streamable-http"},
+	}}, nil)
 	if err != nil {
-		t.Fatalf("renderConfig failed: %v", err)
+		t.Fatal(err)
 	}
-	text := string(rendered)
-	want := "  gateway:\n    url: \"http://task-sandbox:10086/sse\"\n    transport: \"sse\"\n    timeout: 1200\n"
-	if !strings.Contains(text, want) {
-		t.Fatalf("rendered config missing the gateway entry %q:\n%s", want, text)
+	want := map[string]any{
+		"gateway":   map[string]any{"url": "http://task-sandbox:10086/sse", "transport": "sse", "timeout": 1200},
+		"streaming": map[string]any{"url": "https://mcp.example.com/mcp"},
 	}
-	// streamable-http is Hermes's default, so it is left implicit.
-	if !strings.Contains(text, "  streaming:\n    url: \"https://mcp.example.com/mcp\"\n") || strings.Count(text, "transport:") != 1 {
-		t.Fatalf("streamable-http server rendered with an explicit transport:\n%s", text)
+	if got := decodeConfigYAML(t, rendered)["mcp_servers"]; !reflect.DeepEqual(got, want) {
+		t.Fatalf("MCP servers = %#v, want %#v", got, want)
 	}
 }
 
@@ -565,29 +498,38 @@ func TestRenderConfig_MCPServerTransportAndTimeout(t *testing.T) {
 // the MCP servers; the default is unchanged.
 func TestRenderConfig_NoSandboxToolsLeavesOnlyMCPAndWeb(t *testing.T) {
 	servers := []core.MCPServerConfig{{Name: "toolathlon", URL: "http://task-sandbox:10086/sse", Transport: "sse"}}
-	render := func(withheld, web bool) string {
-		t.Helper()
-		rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 10, webSearchEnabled: web, mcpServers: servers, noSandboxTools: withheld}, nil)
+	for _, test := range []struct {
+		withheld, web      bool
+		toolsets, disabled []any
+	}{
+		{true, false, []any{}, []any{"delegation", "terminal", "file", "code_execution"}},
+		{true, true, []any{"web"}, []any{"delegation", "terminal", "file", "code_execution"}},
+		{false, false, []any{"terminal", "file", "code_execution"}, []any{"delegation"}},
+	} {
+		rendered, err := renderConfig(validModel(), renderSettings{maxTurns: 10, webSearchEnabled: test.web, mcpServers: servers, noSandboxTools: test.withheld}, nil)
 		if err != nil {
 			t.Fatal(err)
 		}
-		return string(rendered)
-	}
-	text := render(true, false)
-	for _, want := range []string{
-		"\n  disabled_toolsets:\n    - delegation\n    - terminal\n    - file\n    - code_execution\n",
-		"\nplatform_toolsets:\n  api_server: []\n",
-		"\nmcp_servers:\n  toolathlon:\n",
-	} {
-		if !strings.Contains(text, want) {
-			t.Fatalf("rendered config lacks %q:\n%s", want, text)
+		config := decodeConfigYAML(t, rendered)
+		tools := config["platform_toolsets"].(map[string]any)["api_server"]
+		disabled := config["agent"].(map[string]any)["disabled_toolsets"]
+		if !reflect.DeepEqual(tools, test.toolsets) || !reflect.DeepEqual(disabled, test.disabled) {
+			t.Fatalf("tools/denylist = %#v / %#v", tools, disabled)
+		}
+		if _, ok := config["mcp_servers"].(map[string]any)["toolathlon"]; !ok {
+			t.Fatal("missing task MCP server")
+		}
+		if _, ok := config["web"]; ok != test.web {
+			t.Fatalf("web selection = %#v", config["web"])
 		}
 	}
-	if text := render(true, true); !strings.Contains(text, "\nplatform_toolsets:\n  api_server:\n    - web\n\nweb:\n") {
-		t.Fatalf("web search not kept on its own:\n%s", text)
-	}
-	if text := render(false, false); !strings.Contains(text, "\n  disabled_toolsets:\n    - delegation\n\n") ||
-		!strings.Contains(text, "\nplatform_toolsets:\n  api_server:\n    - terminal\n    - file\n    - code_execution\n") {
-		t.Fatalf("the default toolsets changed:\n%s", text)
+}
+
+func decodeConfigYAML(t *testing.T, rendered []byte) map[string]any {
+	t.Helper()
+	var config map[string]any
+	if err := yaml.Unmarshal(rendered, &config); err != nil {
+		t.Fatalf("invalid YAML: %v\n%s", err, rendered)
 	}
+	return config
 }
diff --git a/pkg/harness/hermes/harness.go b/pkg/harness/hermes/harness.go
index 83977a4d..4c759dc0 100644
--- a/pkg/harness/hermes/harness.go
+++ b/pkg/harness/hermes/harness.go
@@ -424,7 +424,6 @@ type voiceSTTResult struct {
 	RawResult     map[string]any `json:"raw_result,omitempty"`
 	Stdout        string         `json:"stdout"`
 	Stderr        string         `json:"stderr"`
-	Signature     string         `json:"signature,omitempty"`
 	Error         string         `json:"error,omitempty"`
 }
 
@@ -492,13 +491,23 @@ func (manager *Manager) transcribeVoice(ctx context.Context, active *session) vo
 		return stt
 	}
 	stt.RawResult = payload
-	if success, ok := payload["success"].(bool); ok && !success {
-		stt.Error = cmp.Or(normalizeTranscript(payload["error"]), "stt_failed")
+	success, ok := payload["success"].(bool)
+	if !ok {
+		stt.Error = "stt_invalid_result"
+		return stt
+	}
+	if !success {
+		nativeError, _ := payload["error"].(string)
+		stt.Error = cmp.Or(nativeError, "stt_failed")
+		return stt
+	}
+	transcript, ok := payload["transcript"].(string)
+	if !ok {
+		stt.Error = "stt_invalid_result"
 		return stt
 	}
-	stt.Transcript = strings.TrimSpace(normalizeTranscript(payload["transcript"]))
+	stt.Transcript = strings.TrimSpace(transcript)
 	stt.RawTranscript = stt.Transcript
-	stt.Signature, _ = payload["signature"].(string)
 	if stt.Transcript == "" {
 		stt.Error = "stt_empty_transcript"
 		return stt
@@ -508,67 +517,22 @@ func (manager *Manager) transcribeVoice(ctx context.Context, active *session) vo
 }
 
 func hermesSTTCommand(options VoiceSTTOptions) []string {
-	provider := options.Provider
-	if provider == "" {
-		provider = "openai"
-	}
-	model := options.Model
-	if model == "" {
-		if provider == "local" {
-			model = "base"
-		} else {
-			model = "gpt-4o-mini-transcribe"
-		}
-	}
 	script := `set -eu
 if [ -f ` + voiceKeyPath + ` ]; then
   OPENAI_API_KEY="$(cat ` + voiceKeyPath + `)"
   export OPENAI_API_KEY
 fi
-exec python3 -c "$1" "$2" "$3" "$4" "$5"
+exec python3 -c "$1" "$2" "$3"
 `
-	return []string{"/bin/sh", "-c", script, "aries-hermes-stt", hermesSTTScript, voiceWAVPath, model, provider, options.Language}
+	return []string{"/bin/sh", "-c", script, "aries-hermes-stt", hermesSTTScript, voiceWAVPath, options.Model}
 }
 
 const hermesSTTScript = `
-import inspect
 import json
-import os
 import sys
 from tools.voice_mode import transcribe_recording
-wav_path = sys.argv[1]
-model = sys.argv[2]
-provider = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("HERMES_STT_PROVIDER", "openai")
-language = sys.argv[4] if len(sys.argv) > 4 else os.environ.get("HERMES_STT_LANGUAGE", "")
-os.environ["HERMES_STT_PROVIDER"] = provider
-os.environ["HERMES_STT_MODEL"] = model
-os.environ["OPENAI_STT_MODEL"] = model
-os.environ["OPENAI_TRANSCRIBE_MODEL"] = model
-if language:
-    os.environ["HERMES_STT_LANGUAGE"] = language
-sig = inspect.signature(transcribe_recording)
-kwargs = {}
-params = list(sig.parameters.values())
-if not params:
-    result = transcribe_recording()
-else:
-    first = params[0].name
-    kwargs[first] = wav_path
-    if "provider" in sig.parameters:
-        kwargs["provider"] = provider
-    if "model" in sig.parameters:
-        kwargs["model"] = model
-    if "language" in sig.parameters and language:
-        kwargs["language"] = language
-    result = transcribe_recording(**kwargs)
-if isinstance(result, str):
-    payload = {"transcript": result}
-elif isinstance(result, dict):
-    payload = result
-else:
-    payload = {"transcript": getattr(result, "text", None) or getattr(result, "transcript", None) or str(result)}
-payload.setdefault("signature", str(sig))
-print(json.dumps(payload, ensure_ascii=False))
+result = transcribe_recording(sys.argv[1], model=sys.argv[2])
+print(json.dumps(result, ensure_ascii=False))
 `
 
 func (manager *Manager) writeVoiceResult(active *session, originalPrompt string, stt voiceSTTResult, agentOutput string) error {
@@ -864,23 +828,6 @@ func lastJSONObject(text string) (map[string]any, bool) {
 	return nil, false
 }
 
-func normalizeTranscript(value any) string {
-	switch typed := value.(type) {
-	case string:
-		return typed
-	case map[string]any:
-		for _, key := range []string{"text", "transcript", "output_text"} {
-			if text, ok := typed[key].(string); ok {
-				return text
-			}
-		}
-	}
-	if value == nil {
-		return ""
-	}
-	return fmt.Sprint(value)
-}
-
 func tailString(content []byte, limit int) string {
 	if limit <= 0 {
 		return ""
diff --git a/pkg/harness/hermes/harness_test.go b/pkg/harness/hermes/harness_test.go
index eb511928..eb3651cc 100644
--- a/pkg/harness/hermes/harness_test.go
+++ b/pkg/harness/hermes/harness_test.go
@@ -8,11 +8,11 @@ import (
 	"context"
 	"encoding/json"
 	"errors"
-	"fmt"
 	"io"
 	"net/http"
 	"net/http/httptest"
 	"os"
+	"os/exec"
 	"path/filepath"
 	"slices"
 	"strconv"
@@ -370,9 +370,9 @@ func TestStartNamesTheBridgeWorkdirToTheTerminal(t *testing.T) {
 	if err != nil {
 		t.Fatal(err)
 	}
-	want := fmt.Sprintf("\nterminal:\n  backend: \"ssh\"\n  cwd: \"/app\"\n  timeout: %d\n", manager.options.TerminalTimeout)
-	if !strings.Contains(string(retained), want) {
-		t.Fatalf("config.yaml lacks the terminal section %q:\n%s", want, retained)
+	terminal := decodeConfigYAML(t, retained)["terminal"].(map[string]any)
+	if terminal["backend"] != "ssh" || terminal["cwd"] != "/app" || terminal["timeout"] != manager.options.TerminalTimeout {
+		t.Fatalf("terminal settings = %#v", terminal)
 	}
 	if !slices.Contains(fake.created.Env, "TERMINAL_CWD=/app") {
 		t.Fatalf("TERMINAL_CWD does not name the bridge's workdir: %v", fake.created.Env)
@@ -485,7 +485,7 @@ func TestStartStagesExtractKeyWhenConfigured(t *testing.T) {
 	if bytes.Contains(retained, extractSecret) {
 		t.Fatalf("extract secret leaked into the retained config:\n%s", retained)
 	}
-	if !bytes.Contains(retained, []byte(`extract_backend: "tavily"`)) {
+	if decodeConfigYAML(t, retained)["web"].(map[string]any)["extract_backend"] != "tavily" {
 		t.Fatalf("retained config is missing extract_backend:\n%s", retained)
 	}
 }
@@ -562,7 +562,7 @@ func TestVoiceTranscribeSynthesizesAudioAndRunsTranscriptAsAgentMessage(t *testi
 	modelSecret := []byte("model-secret")
 	voiceSecret := []byte("voice-secret")
 	fake := newFakeDeployment(t)
-	fake.sttStdout = `{"transcript":"fix the repository from speech","signature":"transcribe_recording(wav_path, provider=None, model=None)"}` + "\n"
+	fake.sttStdout = `{"success":true,"transcript":"fix the repository from speech"}` + "\n"
 	manager, err := New(Options{Runtime: harnesscommon.RuntimeOptions{
 
 		Deployment:   fake,
@@ -616,8 +616,9 @@ func TestVoiceTranscribeSynthesizesAudioAndRunsTranscriptAsAgentMessage(t *testi
 	if err != nil {
 		t.Fatal(err)
 	}
-	if !bytes.Contains(retainedConfig, []byte("provider: \"openai\"")) || !bytes.Contains(retainedConfig, []byte("model: \"gpt-4o-mini-transcribe\"")) {
-		t.Fatalf("config is missing voice STT settings:\n%s", retainedConfig)
+	sttConfig := decodeConfigYAML(t, retainedConfig)["stt"].(map[string]any)
+	if sttConfig["provider"] != "openai" || sttConfig["openai"].(map[string]any)["model"] != "gpt-4o-mini-transcribe" || sttConfig["local"].(map[string]any)["language"] != "en" {
+		t.Fatalf("voice STT settings = %#v", sttConfig)
 	}
 
 	runtimeEntries := archiveContents(t, runtimeArchive)
@@ -639,7 +640,7 @@ func TestVoiceTranscribeSynthesizesAudioAndRunsTranscriptAsAgentMessage(t *testi
 			sttCmd = append([]string{options.Path}, options.Args...)
 		}
 	}
-	if len(sttCmd) != 9 || sttCmd[5] != voiceWAVPath || sttCmd[6] != "gpt-4o-mini-transcribe" || sttCmd[7] != "openai" || sttCmd[8] != "en" {
+	if len(sttCmd) != 7 || sttCmd[5] != voiceWAVPath || sttCmd[6] != "gpt-4o-mini-transcribe" {
 		t.Fatalf("stt exec argv = %#v", sttCmd)
 	}
 	if !slices.Equal(fake.gatewayInputs, []string{"fix the repository from speech"}) {
@@ -681,7 +682,7 @@ func TestVoiceTranscribeMapsOpenAICompatibleAgentProvider(t *testing.T) {
 	} {
 		t.Run(tc.name, func(t *testing.T) {
 			fake := newFakeDeployment(t)
-			fake.sttStdout = `{"transcript":"fix from speech"}` + "\n"
+			fake.sttStdout = `{"success":true,"transcript":"fix from speech"}` + "\n"
 			manager, err := New(Options{Runtime: harnesscommon.RuntimeOptions{
 
 				Deployment:   fake,
@@ -721,7 +722,7 @@ func TestVoiceTranscribeMapsOpenAICompatibleAgentProvider(t *testing.T) {
 			if err != nil {
 				t.Fatal(err)
 			}
-			if !bytes.Contains(config, []byte(`provider: "custom"`)) {
+			if decodeConfigYAML(t, config)["model"].(map[string]any)["provider"] != "custom" {
 				t.Fatalf("Gateway model provider not mapped: %s", config)
 			}
 			if err := manager.Stop(context.Background()); err != nil {
@@ -731,6 +732,97 @@ func TestVoiceTranscribeMapsOpenAICompatibleAgentProvider(t *testing.T) {
 	}
 }
 
+func TestHermesSTTScriptUsesPinnedSignature(t *testing.T) {
+	python, err := exec.LookPath("python3")
+	if err != nil {
+		t.Skip("python3 is required to exercise the embedded native STT adapter")
+	}
+	root := t.TempDir()
+	toolsDir := filepath.Join(root, "tools")
+	if err := os.Mkdir(toolsDir, 0o700); err != nil {
+		t.Fatal(err)
+	}
+	stub := `def transcribe_recording(wav_path, model=None):
+    assert wav_path == "/recording.wav"
+    assert model == "gpt-4o-mini-transcribe"
+    return {"success": True, "transcript": "fix from speech", "provider": "openai"}
+`
+	if err := os.WriteFile(filepath.Join(toolsDir, "voice_mode.py"), []byte(stub), 0o600); err != nil {
+		t.Fatal(err)
+	}
+	command := exec.Command(python, "-c", hermesSTTScript, "/recording.wav", "gpt-4o-mini-transcribe")
+	command.Dir = root
+	output, err := command.CombinedOutput()
+	if err != nil {
+		t.Fatalf("STT adapter: %v\n%s", err, output)
+	}
+	var payload map[string]any
+	if err := json.Unmarshal(output, &payload); err != nil {
+		t.Fatal(err)
+	}
+	if payload["success"] != true || payload["transcript"] != "fix from speech" || payload["provider"] != "openai" || len(payload) != 3 {
+		t.Fatalf("native result was changed: %#v", payload)
+	}
+}
+
+func TestVoiceTranscribeRejectsInvalidNativeResults(t *testing.T) {
+	for _, test := range []struct{ name, payload, wantError string }{
+		{"missing success", `{"transcript":"invented result"}`, "stt_invalid_result"},
+		{"invalid success", `{"success":"true","transcript":"invented result"}`, "stt_invalid_result"},
+		{"object transcript", `{"success":true,"transcript":{"text":"invented result"}}`, "stt_invalid_result"},
+		{"numeric transcript", `{"success":true,"transcript":123}`, "stt_invalid_result"},
+		{"string result", `"invented result"`, "stt_no_json_result"},
+		{"filtered hallucination", `{"success":true,"transcript":"","filtered":true}`, "stt_empty_transcript"},
+		{"native failure", `{"success":false,"transcript":"","error":"provider failed"}`, "provider failed"},
+	} {
+		t.Run(test.name, func(t *testing.T) {
+			fake := newFakeDeployment(t)
+			fake.sttStdout = test.payload + "\n"
+			manager, err := New(Options{
+				Runtime: harnesscommon.RuntimeOptions{
+					Deployment: fake, Image: testHermesImage, OutputDir: t.TempDir(),
+					StartTimeout: 2 * time.Second, AgentTimeout: 2 * time.Second,
+					APIKeyLookup: func(string) ([]byte, bool) { return []byte("private-key"), true },
+				},
+				Common:          harnesscommon.Options{Mode: ModeVoiceTranscribe},
+				VoiceTranscribe: VoiceTranscribeOptions{STT: VoiceSTTOptions{Timeout: time.Second}},
+			})
+			if err != nil {
+				t.Fatal(err)
+			}
+			manager.newSpeech = func(audioinput.SpeechClientOptions) (speechSynthesizer, error) {
+				return stubSpeechSynthesizer{}, nil
+			}
+			if err := manager.Start(context.Background(), testRequest(t)); err != nil {
+				t.Fatal(err)
+			}
+			defer manager.Stop(context.Background())
+			result, err := manager.Run(context.Background(), "original task instruction")
+			if err == nil || !strings.Contains(err.Error(), test.wantError) || result.Status != core.StatusFailed {
+				t.Fatalf("STT result = %#v, error = %v", result, err)
+			}
+			if len(fake.gatewayInputs) != 0 {
+				t.Fatalf("failed STT started an agent: %#v", fake.gatewayInputs)
+			}
+		})
+	}
+}
+
+func TestVoiceTranscribePreservesCancellation(t *testing.T) {
+	fake := newFakeDeployment(t)
+	manager := newTestManager(t, fake, []byte("private-key"))
+	if err := manager.Start(context.Background(), testRequest(t)); err != nil {
+		t.Fatal(err)
+	}
+	defer manager.Stop(context.Background())
+	ctx, cancel := context.WithCancel(context.Background())
+	cancel()
+	result := manager.transcribeVoice(ctx, manager.active)
+	if result.OK || result.Error != context.Canceled.Error() {
+		t.Fatalf("canceled STT result = %#v", result)
+	}
+}
+
 func TestRunAcceptsExactlyOneInstruction(t *testing.T) {
 	fake := newFakeDeployment(t)
 	manager := newTestManager(t, fake, []byte("model-secret"))
@@ -1267,8 +1359,9 @@ func TestStartRendersTheTaskMCPServers(t *testing.T) {
 	if err != nil {
 		t.Fatal(err)
 	}
-	if want := "  toolathlon:\n    url: \"http://sandbox-a:10086/sse\"\n    transport: \"sse\"\n    timeout: 1200\n"; !strings.Contains(string(retained), want) {
-		t.Fatalf("config.yaml lacks the task's server %q:\n%s", want, retained)
+	server := decodeConfigYAML(t, retained)["mcp_servers"].(map[string]any)["toolathlon"].(map[string]any)
+	if server["url"] != "http://sandbox-a:10086/sse" || server["transport"] != "sse" || server["timeout"] != 1200 {
+		t.Fatalf("task MCP server = %#v", server)
 	}
 
 	clash := newFakeDeployment(t)
diff --git a/pkg/harness/hermes/temperature_integration_test.go b/pkg/harness/hermes/temperature_integration_test.go
index 13e97ef1..6e2c4c21 100644
--- a/pkg/harness/hermes/temperature_integration_test.go
+++ b/pkg/harness/hermes/temperature_integration_test.go
@@ -80,7 +80,7 @@ func TestRequestSettingsReachRealHermes(t *testing.T) {
 				StartTimeout:   90 * time.Second,
 				CleanupTimeout: 60 * time.Second,
 				APIKeyLookup:   func(string) ([]byte, bool) { return []byte("sk-integration-not-a-real-key"), true },
-			}, ExtraBody: []byte(`{"user":"aries-temperature-regression"}`)})
+			}, ExtraBody: []byte(`{"user":"aries-temperature-regression","metadata":{"integer":9007199254740993,"huge":18446744073709551617,"scientific":1e3,"run":"${ARIES_RUN_ID}","nested":["a: b","line\nbreak",null]}}`)})
 			if err != nil {
 				t.Fatal(err)
 			}
@@ -134,6 +134,22 @@ func TestRequestSettingsReachRealHermes(t *testing.T) {
 				if string(body["user"]) != `"aries-temperature-regression"` {
 					t.Errorf("extra body user=%s", body["user"])
 				}
+				var metadata map[string]json.RawMessage
+				if err := json.Unmarshal(body["metadata"], &metadata); err != nil {
+					t.Fatal(err)
+				}
+				for key, want := range map[string]string{
+					"integer": "9007199254740993", "huge": "18446744073709551617",
+					"scientific": "1000.0", "run": `"temperature-integration"`,
+				} {
+					if string(metadata[key]) != want {
+						t.Errorf("metadata.%s=%s, want %s", key, metadata[key], want)
+					}
+				}
+				var nested []any
+				if err := json.Unmarshal(metadata["nested"], &nested); err != nil || len(nested) != 3 || nested[0] != "a: b" || nested[1] != "line\nbreak" || nested[2] != nil {
+					t.Errorf("nested extra body=%s (%v)", metadata["nested"], err)
+				}
 				if string(body["reasoning_effort"]) != fmt.Sprintf("%q", wireReasoning) {
 					t.Errorf("reasoning_effort=%s, want %s", body["reasoning_effort"], wireReasoning)
 				}
diff --git a/pkg/harness/openclaw/gateway/websocket.go b/pkg/harness/openclaw/gateway/websocket.go
index 948addd5..a1d73037 100644
--- a/pkg/harness/openclaw/gateway/websocket.go
+++ b/pkg/harness/openclaw/gateway/websocket.go
@@ -1,56 +1,23 @@
 package gateway
 
 import (
-	"bufio"
-	"bytes"
 	"context"
-	"crypto/rand"
-	"crypto/sha1"
-	"crypto/tls"
-	"encoding/base64"
-	"encoding/binary"
 	"errors"
 	"fmt"
 	"io"
 	"net"
-	"net/http"
 	"net/url"
 	"strings"
 	"sync"
-	"time"
 	"unicode/utf8"
-)
-
-const websocketGUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
 
-type webSocketProtocolViolation string
-
-const (
-	webSocketReservedBits    webSocketProtocolViolation = "reserved bits"
-	webSocketFragmentation   webSocketProtocolViolation = "fragmentation"
-	webSocketInvalidOpcode   webSocketProtocolViolation = "invalid opcode"
-	webSocketMaskDirection   webSocketProtocolViolation = "invalid mask direction"
-	webSocketInvalidFraming  webSocketProtocolViolation = "invalid framing"
-	webSocketMessageTooLarge webSocketProtocolViolation = "message too large"
-	webSocketInvalidControl  webSocketProtocolViolation = "invalid control frame"
-	webSocketInvalidClose    webSocketProtocolViolation = "invalid close frame"
+	"github.com/gorilla/websocket"
 )
 
-type webSocketProtocolError struct {
-	violation webSocketProtocolViolation
-}
-
-func (err *webSocketProtocolError) Error() string {
-	return "gateway websocket protocol violation: " + string(err.violation)
-}
-
-func newWebSocketProtocolError(violation webSocketProtocolViolation) error {
-	return &webSocketProtocolError{violation: violation}
-}
+var errWebSocketProtocol = errors.New("gateway websocket protocol violation")
 
 func isWebSocketProtocolError(err error) bool {
-	var protocolErr *webSocketProtocolError
-	return errors.As(err, &protocolErr)
+	return errors.Is(err, errWebSocketProtocol)
 }
 
 type WebSocketOptions struct {
@@ -58,8 +25,7 @@ type WebSocketOptions struct {
 }
 
 type webSocketTransport struct {
-	connection net.Conn
-	reader     *bufio.Reader
+	connection *websocket.Conn
 	mu         sync.Mutex
 	closeOnce  sync.Once
 	closeErr   error
@@ -72,7 +38,7 @@ func NewWebSocketDialer(options WebSocketOptions) (DialFunc, error) {
 	}
 	parsed, err := url.Parse(rawURL)
 	if err != nil {
-		return nil, fmt.Errorf("parse gateway websocket URL: %w", err)
+		return nil, errors.New("invalid gateway websocket URL")
 	}
 	if parsed.Scheme != "ws" && parsed.Scheme != "wss" {
 		return nil, fmt.Errorf("gateway websocket URL must use ws or wss")
@@ -81,140 +47,99 @@ func NewWebSocketDialer(options WebSocketOptions) (DialFunc, error) {
 		return nil, fmt.Errorf("gateway websocket URL missing host")
 	}
 	return func(ctx context.Context) (Transport, error) {
-		return dialWebSocket(ctx, parsed)
-	}, nil
-}
-
-func dialWebSocket(ctx context.Context, endpoint *url.URL) (*webSocketTransport, error) {
-	connection, err := dialWebSocketConnection(ctx, endpoint)
-	if err != nil {
-		return nil, err
-	}
-	key, err := websocketKey()
-	if err != nil {
-		connection.Close()
-		return nil, err
-	}
-	if deadline, ok := ctx.Deadline(); ok {
-		connection.SetDeadline(deadline)
-		defer connection.SetDeadline(time.Time{})
-	}
-	path := endpoint.RequestURI()
-	if path == "" {
-		path = "/"
-	}
-	request := bytes.NewBuffer(nil)
-	fmt.Fprintf(request, "GET %s HTTP/1.1\r\n", path)
-	fmt.Fprintf(request, "Host: %s\r\n", endpoint.Host)
-	fmt.Fprintf(request, "Upgrade: websocket\r\n")
-	fmt.Fprintf(request, "Connection: Upgrade\r\n")
-	fmt.Fprintf(request, "Sec-WebSocket-Key: %s\r\n", key)
-	fmt.Fprintf(request, "Sec-WebSocket-Version: 13\r\n")
-	fmt.Fprintf(request, "\r\n")
-	if _, err := connection.Write(request.Bytes()); err != nil {
-		connection.Close()
-		return nil, fmt.Errorf("write gateway websocket handshake: %w", err)
-	}
-	reader := bufio.NewReader(connection)
-	response, err := http.ReadResponse(reader, &http.Request{Method: http.MethodGet})
-	if err != nil {
-		connection.Close()
-		return nil, fmt.Errorf("read gateway websocket handshake: %w", err)
-	}
-	defer response.Body.Close()
-	if response.StatusCode != http.StatusSwitchingProtocols {
-		connection.Close()
-		return nil, fmt.Errorf("gateway websocket handshake returned %s", response.Status)
-	}
-	if !headerToken(response.Header, "Upgrade", "websocket") || !headerToken(response.Header, "Connection", "upgrade") {
-		connection.Close()
-		return nil, fmt.Errorf("gateway websocket handshake missing upgrade headers")
-	}
-	if response.Header.Get("Sec-WebSocket-Accept") != websocketAccept(key) {
-		connection.Close()
-		return nil, fmt.Errorf("gateway websocket handshake returned invalid accept key")
-	}
-	return &webSocketTransport{connection: connection, reader: reader}, nil
-}
-
-func dialWebSocketConnection(ctx context.Context, endpoint *url.URL) (net.Conn, error) {
-	address := endpoint.Host
-	if endpoint.Port() == "" {
-		if endpoint.Scheme == "wss" {
-			address = net.JoinHostPort(endpoint.Hostname(), "443")
-		} else {
-			address = net.JoinHostPort(endpoint.Hostname(), "80")
+		// DialContext bounds connection establishment and TLS. Closing the socket
+		// also interrupts an HTTP upgrade when cancellation has no deadline.
+		stop := func() bool { return true }
+		dialer := websocket.Dialer{NetDialContext: func(ctx context.Context, network, address string) (net.Conn, error) {
+			connection, err := (&net.Dialer{}).DialContext(ctx, network, address)
+			if err == nil {
+				stop = context.AfterFunc(ctx, func() { _ = connection.Close() })
+			}
+			return connection, err
+		}}
+		connection, response, err := dialer.DialContext(ctx, rawURL, nil)
+		stop()
+		if response != nil {
+			_ = response.Body.Close()
+		}
+		if ctx.Err() != nil {
+			if connection != nil {
+				_ = connection.Close()
+			}
+			return nil, ctx.Err()
 		}
-	}
-	dialer := net.Dialer{}
-	if endpoint.Scheme != "wss" {
-		connection, err := dialer.DialContext(ctx, "tcp", address)
 		if err != nil {
-			return nil, fmt.Errorf("dial gateway websocket: %w", err)
+			// Upgrade responses and URL errors may contain credentials.
+			return nil, errors.New("gateway websocket handshake failed")
 		}
-		return connection, nil
-	}
-	tlsDialer := tls.Dialer{NetDialer: &dialer, Config: &tls.Config{ServerName: endpoint.Hostname()}}
-	connection, err := tlsDialer.DialContext(ctx, "tcp", address)
-	if err != nil {
-		return nil, fmt.Errorf("dial gateway websocket TLS: %w", err)
-	}
-	return connection, nil
+		connection.SetReadLimit(maxMessageBytes)
+		return &webSocketTransport{connection: connection}, nil
+	}, nil
 }
 
 func (transport *webSocketTransport) Send(ctx context.Context, content []byte) error {
 	if transport == nil || transport.connection == nil {
-		return fmt.Errorf("gateway websocket is not connected")
+		return errors.New("gateway websocket is not connected")
 	}
-	frame, err := encodeClientWebSocketFrame(1, content)
-	if err != nil {
+	if len(content) > maxMessageBytes {
+		return errors.New("gateway websocket message too large")
+	}
+	if err := ctx.Err(); err != nil {
 		return err
 	}
+	stop := context.AfterFunc(ctx, func() { _ = transport.Close() })
+	defer stop()
 	transport.mu.Lock()
 	defer transport.mu.Unlock()
-	if deadline, ok := ctx.Deadline(); ok {
-		transport.connection.SetWriteDeadline(deadline)
-		defer transport.connection.SetWriteDeadline(time.Time{})
+	if err := ctx.Err(); err != nil {
+		return err
 	}
-	if _, err := transport.connection.Write(frame); err != nil {
-		return fmt.Errorf("write gateway websocket frame: %w", err)
+	if err := transport.connection.WriteMessage(websocket.TextMessage, content); err != nil {
+		if ctx.Err() != nil {
+			return ctx.Err()
+		}
+		return errors.New("write gateway websocket message failed")
 	}
 	return nil
 }
 
 func (transport *webSocketTransport) Receive(ctx context.Context) ([]byte, error) {
 	if transport == nil || transport.connection == nil {
-		return nil, fmt.Errorf("gateway websocket is not connected")
+		return nil, errors.New("gateway websocket is not connected")
 	}
-	if deadline, ok := ctx.Deadline(); ok {
-		transport.connection.SetReadDeadline(deadline)
-		defer transport.connection.SetReadDeadline(time.Time{})
+	if err := ctx.Err(); err != nil {
+		return nil, err
 	}
-	for {
-		opcode, payload, err := readWebSocketFrameWithMask(transport.reader, false)
+	stop := context.AfterFunc(ctx, func() { _ = transport.Close() })
+	defer stop()
+	typ, reader, err := transport.connection.NextReader()
+	var content []byte
+	if err == nil {
+		content, err = io.ReadAll(reader)
 		if err != nil {
-			if ctx.Err() != nil {
-				return nil, ctx.Err()
-			}
-			return nil, err
+			// A connection lost inside a message cannot validate queued results.
+			err = errWebSocketProtocol
 		}
-		switch opcode {
-		case 1, 2:
-			return payload, nil
-		case 8:
-			if err := validateClosePayload(payload); err != nil {
-				return nil, err
-			}
+	}
+	if ctx.Err() != nil {
+		return nil, ctx.Err()
+	}
+	if err != nil {
+		// Close reasons and library protocol diagnostics must not expose peer
+		// content. Ordinary disconnections still allow queued complete events.
+		var closeErr *websocket.CloseError
+		var netErr net.Error
+		if errors.As(err, &closeErr) || errors.As(err, &netErr) || errors.Is(err, net.ErrClosed) || errors.Is(err, io.EOF) {
 			return nil, io.EOF
-		case 9:
-			if err := transport.writeControl(10, payload); err != nil {
-				return nil, err
-			}
-		case 10:
-		default:
-			return nil, newWebSocketProtocolError(webSocketInvalidOpcode)
 		}
+		return nil, errWebSocketProtocol
+	}
+	// Gorilla leaves text encoding validation to the application. Validate the
+	// assembled message so UTF-8 characters may span continuation frames.
+	if typ == websocket.TextMessage && !utf8.Valid(content) {
+		return nil, errWebSocketProtocol
 	}
+	return content, nil
 }
 
 func (transport *webSocketTransport) Close() error {
@@ -222,173 +147,8 @@ func (transport *webSocketTransport) Close() error {
 		return nil
 	}
 	transport.closeOnce.Do(func() {
+		// Close releases blocked data/control writes without a close handshake.
 		transport.closeErr = transport.connection.Close()
 	})
 	return transport.closeErr
 }
-
-func (transport *webSocketTransport) writeControl(opcode byte, payload []byte) error {
-	frame, err := encodeClientWebSocketFrame(opcode, payload)
-	if err != nil {
-		return err
-	}
-	transport.mu.Lock()
-	defer transport.mu.Unlock()
-	if _, err := transport.connection.Write(frame); err != nil {
-		return fmt.Errorf("write gateway websocket control frame: %w", err)
-	}
-	return nil
-}
-
-func websocketKey() (string, error) {
-	var raw [16]byte
-	if _, err := rand.Read(raw[:]); err != nil {
-		return "", fmt.Errorf("generate gateway websocket key: %w", err)
-	}
-	return base64.StdEncoding.EncodeToString(raw[:]), nil
-}
-
-func websocketAccept(key string) string {
-	sum := sha1.Sum([]byte(key + websocketGUID))
-	return base64.StdEncoding.EncodeToString(sum[:])
-}
-
-func headerToken(headers http.Header, key, token string) bool {
-	for _, value := range headers.Values(key) {
-		for _, part := range strings.Split(value, ",") {
-			if strings.EqualFold(strings.TrimSpace(part), token) {
-				return true
-			}
-		}
-	}
-	return false
-}
-
-func encodeClientWebSocketFrame(opcode byte, payload []byte) ([]byte, error) {
-	if int64(len(payload)) > maxMessageBytes {
-		return nil, fmt.Errorf("gateway websocket message too large: %d bytes", len(payload))
-	}
-	var mask [4]byte
-	if _, err := rand.Read(mask[:]); err != nil {
-		return nil, fmt.Errorf("generate gateway websocket mask: %w", err)
-	}
-	frame := bytes.NewBuffer(nil)
-	frame.WriteByte(0x80 | opcode)
-	switch length := len(payload); {
-	case length < 126:
-		frame.WriteByte(0x80 | byte(length))
-	case length <= 0xffff:
-		frame.WriteByte(0x80 | 126)
-		var encoded [2]byte
-		binary.BigEndian.PutUint16(encoded[:], uint16(length))
-		frame.Write(encoded[:])
-	default:
-		frame.WriteByte(0x80 | 127)
-		var encoded [8]byte
-		binary.BigEndian.PutUint64(encoded[:], uint64(length))
-		frame.Write(encoded[:])
-	}
-	frame.Write(mask[:])
-	for index, value := range payload {
-		frame.WriteByte(value ^ mask[index%len(mask)])
-	}
-	return frame.Bytes(), nil
-}
-
-func readWebSocketFrame(reader *bufio.Reader) (byte, []byte, error) {
-	return readWebSocketFrameWithMask(reader, true)
-}
-
-func readWebSocketFrameWithMask(reader *bufio.Reader, expectMasked bool) (byte, []byte, error) {
-	header, err := reader.ReadByte()
-	if err != nil {
-		return 0, nil, err
-	}
-	if header&0x70 != 0 {
-		return 0, nil, newWebSocketProtocolError(webSocketReservedBits)
-	}
-	if header&0x80 == 0 {
-		return 0, nil, newWebSocketProtocolError(webSocketFragmentation)
-	}
-	opcode := header & 0x0f
-	if opcode != 0x1 && opcode != 0x2 && opcode != 0x8 && opcode != 0x9 && opcode != 0xa {
-		return 0, nil, newWebSocketProtocolError(webSocketInvalidOpcode)
-	}
-	lengthByte, err := reader.ReadByte()
-	if err != nil {
-		return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-	}
-	masked := lengthByte&0x80 != 0
-	if masked != expectMasked {
-		return 0, nil, newWebSocketProtocolError(webSocketMaskDirection)
-	}
-	length := uint64(lengthByte & 0x7f)
-	if opcode >= 0x8 && length >= 126 {
-		return 0, nil, newWebSocketProtocolError(webSocketInvalidControl)
-	}
-	switch length {
-	case 126:
-		var encoded [2]byte
-		if _, err := io.ReadFull(reader, encoded[:]); err != nil {
-			return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-		}
-		length = uint64(binary.BigEndian.Uint16(encoded[:]))
-		if length < 126 {
-			return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-		}
-	case 127:
-		var encoded [8]byte
-		if _, err := io.ReadFull(reader, encoded[:]); err != nil {
-			return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-		}
-		length = binary.BigEndian.Uint64(encoded[:])
-		if length < 65536 || length&(uint64(1)<<63) != 0 {
-			return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-		}
-	}
-	if length > maxMessageBytes {
-		return 0, nil, newWebSocketProtocolError(webSocketMessageTooLarge)
-	}
-	var mask [4]byte
-	if masked {
-		if _, err := io.ReadFull(reader, mask[:]); err != nil {
-			return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-		}
-	}
-	payload := make([]byte, int(length))
-	if _, err := io.ReadFull(reader, payload); err != nil {
-		return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-	}
-	if masked {
-		for index := range payload {
-			payload[index] ^= mask[index%len(mask)]
-		}
-	}
-	if opcode == 1 && !utf8.Valid(payload) {
-		return 0, nil, newWebSocketProtocolError(webSocketInvalidFraming)
-	}
-	return opcode, payload, nil
-}
-
-func validateClosePayload(payload []byte) error {
-	if len(payload) == 1 {
-		return newWebSocketProtocolError(webSocketInvalidClose)
-	}
-	if len(payload) < 2 {
-		return nil
-	}
-	code := binary.BigEndian.Uint16(payload[:2])
-	if !validCloseCode(code) || !utf8.Valid(payload[2:]) {
-		return newWebSocketProtocolError(webSocketInvalidClose)
-	}
-	return nil
-}
-
-func validCloseCode(code uint16) bool {
-	switch code {
-	case 1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014:
-		return true
-	default:
-		return code >= 3000 && code < 5000
-	}
-}
diff --git a/pkg/harness/openclaw/gateway/websocket_test.go b/pkg/harness/openclaw/gateway/websocket_test.go
index ef7278c5..9d082e36 100644
--- a/pkg/harness/openclaw/gateway/websocket_test.go
+++ b/pkg/harness/openclaw/gateway/websocket_test.go
@@ -4,6 +4,8 @@ import (
 	"bufio"
 	"bytes"
 	"context"
+	"crypto/sha1"
+	"encoding/base64"
 	"encoding/binary"
 	"encoding/json"
 	"errors"
@@ -12,9 +14,10 @@ import (
 	"net"
 	"net/http"
 	"strings"
-	"sync"
 	"testing"
 	"time"
+
+	"github.com/gorilla/websocket"
 )
 
 func TestWebSocketDialerConnectsAndCarriesGatewayFrames(t *testing.T) {
@@ -91,7 +94,7 @@ func acceptTestWebSocket(t *testing.T, writer http.ResponseWriter, request *http
 	if key == "" {
 		t.Fatal("missing Sec-WebSocket-Key")
 	}
-	if !headerToken(request.Header, "Connection", "upgrade") || !headerToken(request.Header, "Upgrade", "websocket") {
+	if !strings.EqualFold(request.Header.Get("Connection"), "upgrade") || !strings.EqualFold(request.Header.Get("Upgrade"), "websocket") {
 		t.Fatalf("missing upgrade headers: %#v", request.Header)
 	}
 	hijacker, ok := writer.(http.Hijacker)
@@ -106,7 +109,7 @@ func acceptTestWebSocket(t *testing.T, writer http.ResponseWriter, request *http
 	fmt.Fprintf(response, "HTTP/1.1 101 Switching Protocols\r\n")
 	fmt.Fprintf(response, "Upgrade: websocket\r\n")
 	fmt.Fprintf(response, "Connection: Upgrade\r\n")
-	fmt.Fprintf(response, "Sec-WebSocket-Accept: %s\r\n", websocketAccept(key))
+	fmt.Fprintf(response, "Sec-WebSocket-Accept: %s\r\n", testWebSocketAccept(key))
 	fmt.Fprintf(response, "\r\n")
 	if _, err := connection.Write(response.Bytes()); err != nil {
 		connection.Close()
@@ -160,263 +163,344 @@ func encodeServerTextFrame(payload []byte) []byte {
 	return frame.Bytes()
 }
 
-func TestWebSocketFrameEncodingMasksClientPayload(t *testing.T) {
-	payload := []byte(`{"type":"req"}`)
-	frame, err := encodeClientWebSocketFrame(1, payload)
-	if err != nil {
-		t.Fatalf("encodeClientWebSocketFrame returned error: %v", err)
-	}
-	if len(frame) < 6 || frame[0] != 0x81 || frame[1]&0x80 == 0 {
-		t.Fatalf("client frame header = %#v", frame[:2])
+// Raw peers exercise the library adapter independently, including messages
+// fragmented at a UTF-8 boundary and control frames between continuations.
+func TestWebSocketFragmentationAndPingPong(t *testing.T) {
+	transport, peer, reader := newPipeWebSocket(t)
+	want := []byte("hello 世界")
+	serverDone := make(chan error, 1)
+	go func() {
+		first := encodeServerTextFrame(want[:7])
+		first[0] = 0x01
+		_, err := peer.Write(append(first, 0x89, 0x02, 'h', 'i'))
+		if err != nil {
+			serverDone <- err
+			return
+		}
+		opcode, payload, err := readWebSocketFrame(reader)
+		if err == nil && (opcode != 10 || string(payload) != "hi") {
+			err = fmt.Errorf("pong = %d %q", opcode, payload)
+		}
+		if err == nil {
+			last := encodeServerTextFrame(want[7:])
+			last[0] = 0x80
+			_, err = peer.Write(append([]byte{0x8a, 0}, last...))
+		}
+		serverDone <- err
+	}()
+	ctx, cancel := contextWithTestTimeout()
+	defer cancel()
+	got, err := transport.Receive(ctx)
+	if err != nil || !bytes.Equal(got, want) {
+		t.Fatalf("Receive = %q, %v", got, err)
 	}
-	reader := bufio.NewReader(bytes.NewReader(frame))
-	opcode, decoded, err := readWebSocketFrame(reader)
-	if err != nil {
-		t.Fatalf("readWebSocketFrame returned error: %v", err)
+	if err := <-serverDone; err != nil {
+		t.Fatal(err)
 	}
-	if opcode != 1 || string(decoded) != string(payload) {
-		t.Fatalf("opcode=%d decoded=%s", opcode, decoded)
+}
+
+func TestWebSocketReadLimitCoversAggregateFragments(t *testing.T) {
+	transport, peer, reader := newPipeWebSocket(t)
+	// A smaller limit exercises the same library setting without allocating 64 MiB.
+	transport.connection.SetReadLimit(8)
+	go func() {
+		_, _ = peer.Write([]byte{0x01, 5, '1', '2', '3', '4', '5', 0x80, 4})
+		_, _, _ = readWebSocketFrame(reader) // Consume the library's close frame.
+	}()
+	ctx, cancel := contextWithTestTimeout()
+	defer cancel()
+	if _, err := transport.Receive(ctx); !isWebSocketProtocolError(err) {
+		t.Fatalf("oversized fragmented message error = %v", err)
 	}
-	if _, err := reader.Peek(1); err != io.EOF {
-		t.Fatalf("trailing frame data err = %v", err)
+}
+
+func TestWebSocketTruncatedMessageIsFatal(t *testing.T) {
+	transport, peer, _ := newPipeWebSocket(t)
+	go func() {
+		_, _ = peer.Write([]byte{0x81, 4, 'a'})
+		_ = peer.Close()
+	}()
+	ctx, cancel := contextWithTestTimeout()
+	defer cancel()
+	if content, err := transport.Receive(ctx); content != nil || !isWebSocketProtocolError(err) {
+		t.Fatalf("truncated message = %q, %v", content, err)
 	}
 }
 
-func TestWebSocketRejectsHostileServerFrames(t *testing.T) {
-	tests := []struct {
-		name      string
-		frame     []byte
-		violation webSocketProtocolViolation
-	}{
-		{name: "reserved-bits", frame: []byte{0xc1, 0x00}, violation: webSocketReservedBits},
-		{name: "fragmented", frame: []byte{0x01, 0x00}, violation: webSocketFragmentation},
-		{name: "masked-server-frame", frame: []byte{0x81, 0x80, 0, 0, 0, 0}, violation: webSocketMaskDirection},
-		{name: "invalid-opcode", frame: []byte{0x83, 0x00}, violation: webSocketInvalidOpcode},
-		{name: "truncated-header", frame: []byte{0x81}, violation: webSocketInvalidFraming},
-		{name: "non-minimal-16-bit-length", frame: []byte{0x81, 126, 0, 1, 'x'}, violation: webSocketInvalidFraming},
-		{name: "non-minimal-64-bit-length", frame: []byte{0x81, 127, 0, 0, 0, 0, 0, 0, 0, 1, 'x'}, violation: webSocketInvalidFraming},
-		{name: "oversized-message", frame: []byte{0x81, 0x7f, 0, 0, 0, 0, 4, 0, 0, 1}, violation: webSocketMessageTooLarge},
-		{name: "oversized-control", frame: []byte{0x89, 126}, violation: webSocketInvalidControl},
-		{name: "invalid-text", frame: []byte{0x81, 0x01, 0xff}, violation: webSocketInvalidFraming},
-	}
-	for _, test := range tests {
-		t.Run(test.name, func(t *testing.T) {
-			_, _, err := readWebSocketFrameWithMask(bufio.NewReader(bytes.NewReader(test.frame)), false)
-			var protocolErr *webSocketProtocolError
-			if !errors.As(err, &protocolErr) || protocolErr.violation != test.violation {
-				t.Fatalf("protocol error = %#v, want %q", err, test.violation)
+func TestWebSocketProtocolFailuresAreSecretFree(t *testing.T) {
+	for _, frame := range [][]byte{
+		{0xc1, 0},                // Reserved bit.
+		{0x81, 0x80, 0, 0, 0, 0}, // Wrong mask direction.
+		{0x83, 0},                // Unknown opcode.
+		{0x09, 0},                // Fragmented ping.
+		{0x81, 1, 0xff},          // Invalid UTF-8.
+		{0x88, 3, 0, 1, 'x'},     // Invalid close code.
+	} {
+		t.Run(fmt.Sprintf("%x", frame), func(t *testing.T) {
+			transport, peer, reader := newPipeWebSocket(t)
+			go func() {
+				_, _ = peer.Write(frame)
+				_, _, _ = readWebSocketFrame(reader)
+			}()
+			ctx, cancel := contextWithTestTimeout()
+			defer cancel()
+			if _, err := transport.Receive(ctx); !isWebSocketProtocolError(err) || err.Error() != errWebSocketProtocol.Error() {
+				t.Fatalf("error = %v", err)
 			}
 		})
 	}
 }
 
-func TestWebSocketRejectsInvalidCloseFrames(t *testing.T) {
-	tests := [][]byte{
-		{0},
-		{0, 1},
-		{0x03, 0xed},
-		{0x07, 0xd0},
-		{0x03, 0xe8, 0xff},
-	}
-	for _, payload := range tests {
-		err := validateClosePayload(payload)
-		var protocolErr *webSocketProtocolError
-		if !errors.As(err, &protocolErr) || protocolErr.violation != webSocketInvalidClose {
-			t.Fatalf("close payload %x error = %#v", payload, err)
-		}
-	}
-	for _, payload := range [][]byte{nil, {0x03, 0xe8}, {0x0b, 0xb8, 'o', 'k'}} {
-		if err := validateClosePayload(payload); err != nil {
-			t.Fatalf("valid close payload %x rejected: %v", payload, err)
-		}
+func TestClientWebSocketProtocolViolationDominatesQueuedDelivery(t *testing.T) {
+	for _, kind := range []string{"response", "event"} {
+		t.Run(kind, func(t *testing.T) {
+			wire, peer, reader := newPipeWebSocket(t)
+			release := make(chan struct{})
+			transport := &heldSendTransport{Transport: wire, sent: make(chan []byte, 1), release: release}
+			client, err := New(func(context.Context) (Transport, error) { return transport, nil }, Options{})
+			if err != nil {
+				t.Fatal(err)
+			}
+			client.transport = transport
+			go client.readLoop(context.Background(), transport)
+			ctx, cancel := contextWithTestTimeout()
+			defer cancel()
+			done := make(chan error, 1)
+			frame := Frame{"type": "event", "event": "partial"}
+			if kind == "response" {
+				go func() { _, err := client.Call(ctx, "status", nil); done <- err }()
+				var request Frame
+				if err := json.Unmarshal(<-transport.sent, &request); err != nil {
+					t.Fatal(err)
+				}
+				frame = Frame{"type": "res", "id": request["id"], "ok": true}
+			}
+			content, err := json.Marshal(frame)
+			if err != nil {
+				t.Fatal(err)
+			}
+			go func() {
+				_, _ = peer.Write(append(encodeServerTextFrame(content), 0xc1, 0))
+				_, _, _ = readWebSocketFrame(reader)
+			}()
+			select {
+			case <-client.readerFailed:
+			case <-ctx.Done():
+				t.Fatal(ctx.Err())
+			}
+			fatal := client.FatalError()
+			if !isWebSocketProtocolError(fatal) {
+				t.Fatalf("fatal error = %v", fatal)
+			}
+			close(release)
+			if kind == "response" {
+				if err := <-done; !errors.Is(err, fatal) {
+					t.Fatalf("queued response error = %v", err)
+				}
+			} else {
+				if frame, err := client.RecvEvent(ctx); frame != nil || !errors.Is(err, fatal) {
+					t.Fatalf("queued event = %#v, %v", frame, err)
+				}
+			}
+		})
 	}
 }
 
-func TestClientWebSocketProtocolViolationDominatesQueuedDelivery(t *testing.T) {
-	t.Run("response", func(t *testing.T) {
-		reader, writer := io.Pipe()
-		websocket := &webSocketTransport{connection: discardNetConn{}, reader: bufio.NewReader(reader)}
-		release := make(chan struct{})
-		transport := &heldSendTransport{Transport: websocket, sent: make(chan []byte, 1), release: release}
-		client, err := New(func(context.Context) (Transport, error) { return transport, nil }, Options{})
-		if err != nil {
-			t.Fatal(err)
-		}
-		client.transport = transport
-		go client.readLoop(context.Background(), transport)
-
-		done := make(chan error, 1)
-		go func() { _, err := client.Call(context.Background(), "status", nil); done <- err }()
-		request := decodeGatewayFrame(t, <-transport.sent)
-		response, err := json.Marshal(Frame{"type": "res", "id": request.String("id"), "ok": true})
-		if err != nil {
-			t.Fatal(err)
-		}
-		writeDone := make(chan error, 1)
+func TestClientWebSocketEOFLeavesQueuedCompleteEventNonfatal(t *testing.T) {
+	for _, closeFrame := range [][]byte{nil, append([]byte{0x88, 8, 0x03, 0xe8}, []byte("secret")...)} {
+		transport, peer, reader := newPipeWebSocket(t)
 		go func() {
-			_, err := writer.Write(append(encodeServerTextFrame(response), 0xc1, 0x00))
-			writeDone <- err
+			_, _ = peer.Write(append(encodeServerTextFrame([]byte(`{"type":"event","event":"complete"}`)), closeFrame...))
+			if closeFrame != nil {
+				_, _, _ = readWebSocketFrame(reader)
+			}
+			_ = peer.Close()
 		}()
-		fatal := waitForFatalError(t, client)
-		close(release)
-		if err := <-done; !errors.Is(err, fatal) {
-			t.Fatalf("Call accepted queued response over protocol failure: %v", err)
-		}
-		if err := <-writeDone; err != nil {
-			t.Fatal(err)
-		}
-	})
-
-	t.Run("event", func(t *testing.T) {
-		event, err := json.Marshal(Frame{"type": "event", "event": "partial", "payload": map[string]any{"text": "safe"}})
-		if err != nil {
-			t.Fatal(err)
-		}
-		secret := "auth-secret-must-not-leak"
-		hostile := append([]byte{0xc1, byte(len(secret))}, secret...)
-		content := append(encodeServerTextFrame(event), hostile...)
-		transport := &webSocketTransport{connection: discardNetConn{}, reader: bufio.NewReader(bytes.NewReader(content))}
 		client, err := New(func(context.Context) (Transport, error) { return transport, nil }, Options{})
 		if err != nil {
 			t.Fatal(err)
 		}
 		client.transport = transport
-		go client.readLoop(context.Background(), transport)
-		fatal := waitForFatalError(t, client)
-		if strings.Contains(fatal.Error(), secret) {
-			t.Fatalf("protocol error leaked hostile frame content: %v", fatal)
+		ctx, cancel := contextWithTestTimeout()
+		client.readLoop(ctx, transport)
+		cancel()
+		if err := client.FatalError(); err != nil {
+			t.Fatalf("EOF reported fatal: %v", err)
 		}
 		frame, err := client.RecvEvent(context.Background())
-		if frame != nil || !errors.Is(err, fatal) {
-			t.Fatalf("RecvEvent accepted queued event %#v over protocol failure: %v", frame, err)
+		if err != nil || frame.String("event") != "complete" {
+			t.Fatalf("queued event = %#v, %v", frame, err)
+		}
+		_, err = client.RecvEvent(context.Background())
+		if !errors.Is(err, io.EOF) || strings.Contains(err.Error(), "secret") {
+			t.Fatalf("close error = %v", err)
+		}
+	}
+}
+
+func TestWebSocketCancellationAndCloseUnblockIO(t *testing.T) {
+	for _, operation := range []string{"read", "write", "pong"} {
+		for _, shutdown := range []string{"cancel", "close"} {
+			t.Run(operation+"/"+shutdown, func(t *testing.T) {
+				transport, peer, _ := newPipeWebSocket(t)
+				ctx, cancel := context.WithCancel(context.Background())
+				defer cancel()
+				done := make(chan error, 1)
+				started := make(chan struct{})
+				go func() {
+					if operation == "write" {
+						done <- transport.Send(ctx, []byte("request"))
+						return
+					}
+					close(started)
+					_, err := transport.Receive(ctx)
+					done <- err
+				}()
+				if operation == "pong" {
+					if _, err := peer.Write([]byte{0x89, 1, 'x'}); err != nil {
+						t.Fatal(err)
+					}
+				}
+				if operation != "read" {
+					// Read only a byte: the remaining write is blocked on net.Pipe.
+					if _, err := peer.Read(make([]byte, 1)); err != nil {
+						t.Fatal(err)
+					}
+				} else {
+					<-started
+				}
+				if shutdown == "cancel" {
+					cancel()
+				} else {
+					closed := make(chan error, 1)
+					go func() { closed <- transport.Close() }()
+					select {
+					case err := <-closed:
+						if err != nil {
+							t.Fatal(err)
+						}
+					case <-time.After(time.Second):
+						t.Fatal("Close blocked")
+					}
+					if err := transport.Close(); err != nil {
+						t.Fatalf("repeated Close: %v", err)
+					}
+				}
+				select {
+				case err := <-done:
+					if err == nil || (shutdown == "cancel" && !errors.Is(err, context.Canceled)) {
+						t.Fatalf("operation error = %v", err)
+					}
+				case <-time.After(time.Second):
+					t.Fatal("operation remained blocked")
+				}
+			})
 		}
-	})
+	}
 }
 
-func TestClientWebSocketEOFLeavesQueuedCompleteEventNonfatal(t *testing.T) {
-	event, err := json.Marshal(Frame{"type": "event", "event": "complete"})
+func TestWebSocketDialCancellationDuringUpgrade(t *testing.T) {
+	listener, err := net.Listen("tcp", "127.0.0.1:0")
 	if err != nil {
-		t.Fatal(err)
+		t.Skipf("loopback listener unavailable: %v", err)
 	}
-	transport := &webSocketTransport{connection: discardNetConn{}, reader: bufio.NewReader(bytes.NewReader(encodeServerTextFrame(event)))}
-	client, err := New(func(context.Context) (Transport, error) { return transport, nil }, Options{})
+	defer listener.Close()
+	accepted := make(chan net.Conn, 1)
+	go func() {
+		connection, err := listener.Accept()
+		if err == nil {
+			accepted <- connection
+		}
+	}()
+	dial, err := NewWebSocketDialer(WebSocketOptions{URL: "ws://" + listener.Addr().String()})
 	if err != nil {
 		t.Fatal(err)
 	}
-	client.transport = transport
-	client.readLoop(context.Background(), transport)
-	if err := client.FatalError(); err != nil {
-		t.Fatalf("normal EOF reported fatal: %v", err)
-	}
-	frame, err := client.RecvEvent(context.Background())
-	if err != nil || frame.String("event") != "complete" {
-		t.Fatalf("queued complete event = %#v, %v", frame, err)
+	ctx, cancel := context.WithCancel(context.Background())
+	defer cancel()
+	done := make(chan error, 1)
+	go func() { _, err := dial(ctx); done <- err }()
+	connection := <-accepted
+	defer connection.Close()
+	if _, err := http.ReadRequest(bufio.NewReader(connection)); err != nil {
+		t.Fatal(err)
 	}
-}
-
-func TestWebSocketCloseUnblocksWritesWithoutWaitingForWriterLock(t *testing.T) {
-	t.Run("direct-and-repeated", func(t *testing.T) {
-		connection := newBlockingWriteConn()
-		transport := &webSocketTransport{connection: connection, reader: bufio.NewReader(connection)}
-		done := make(chan error, 1)
-		go func() { done <- transport.Close() }()
-		if err := waitForClose(t, connection, done); err != nil {
+	cancel()
+	select {
+	case err := <-done:
+		if !errors.Is(err, context.Canceled) {
 			t.Fatal(err)
 		}
-		select {
-		case <-connection.writeStarted:
-			t.Fatal("Close attempted a graceful control-frame write before closing the connection")
-		default:
-		}
-		if err := transport.Close(); err != nil {
-			t.Fatalf("repeated Close returned error: %v", err)
-		}
-	})
-
-	tests := []struct {
-		name   string
-		reader []byte
-		write  func(*webSocketTransport) error
-	}{
-		{name: "normal-write", write: func(transport *webSocketTransport) error {
-			return transport.Send(context.Background(), []byte("request"))
-		}},
-		{name: "pong-control-write", reader: []byte{0x89, 0x04, 'p', 'i', 'n', 'g'}, write: func(transport *webSocketTransport) error {
-			_, err := transport.Receive(context.Background())
-			return err
-		}},
-	}
-	for _, test := range tests {
-		t.Run(test.name, func(t *testing.T) {
-			connection := newBlockingWriteConn()
-			reader := io.Reader(connection)
-			if test.reader != nil {
-				reader = bytes.NewReader(test.reader)
-			}
-			transport := &webSocketTransport{connection: connection, reader: bufio.NewReader(reader)}
-			writeDone := make(chan error, 1)
-			go func() { writeDone <- test.write(transport) }()
-			select {
-			case <-connection.writeStarted:
-			case <-time.After(time.Second):
-				t.Fatal("write did not start")
-			}
-			closeDone := make(chan error, 1)
-			go func() { closeDone <- transport.Close() }()
-			if err := waitForClose(t, connection, closeDone); err != nil {
-				t.Fatal(err)
-			}
-			select {
-			case err := <-writeDone:
-				if err == nil || !errors.Is(err, net.ErrClosed) {
-					t.Fatalf("blocked write error = %v", err)
-				}
-			case <-time.After(time.Second):
-				t.Fatal("blocked write goroutine was not released")
-			}
-		})
+	case <-time.After(time.Second):
+		t.Fatal("upgrade ignored cancellation")
 	}
 }
 
-func waitForClose(t *testing.T, connection *blockingWriteConn, done <-chan error) error {
+func newPipeWebSocket(t *testing.T) (*webSocketTransport, net.Conn, *bufio.Reader) {
 	t.Helper()
-	select {
-	case err := <-done:
-		return err
-	case <-time.After(100 * time.Millisecond):
-		connection.forceClose()
-		<-done
-		t.Fatal("Close waited for a blocked WebSocket write")
-		return nil
+	client, peer := net.Pipe()
+	t.Cleanup(func() { _ = client.Close(); _ = peer.Close() })
+	_ = peer.SetDeadline(time.Now().Add(5 * time.Second))
+	reader := bufio.NewReader(peer)
+	go func() {
+		request, err := http.ReadRequest(reader)
+		if err != nil {
+			return
+		}
+		_, _ = fmt.Fprintf(peer, "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n", testWebSocketAccept(request.Header.Get("Sec-WebSocket-Key")))
+	}()
+	dialer := websocket.Dialer{NetDialContext: func(context.Context, string, string) (net.Conn, error) { return client, nil }}
+	ctx, cancel := contextWithTestTimeout()
+	defer cancel()
+	connection, response, err := dialer.DialContext(ctx, "ws://test", nil)
+	if response != nil {
+		_ = response.Body.Close()
+	}
+	if err != nil {
+		t.Fatal(err)
 	}
+	connection.SetReadLimit(maxMessageBytes)
+	transport := &webSocketTransport{connection: connection}
+	t.Cleanup(func() { _ = transport.Close() })
+	return transport, peer, reader
 }
 
-func waitForFatalError(t *testing.T, client *Client) error {
-	t.Helper()
-	deadline := time.Now().Add(time.Second)
-	for time.Now().Before(deadline) {
-		if err := client.FatalError(); err != nil {
-			if !isWebSocketProtocolError(err) {
-				t.Fatalf("fatal error is not classified: %v", err)
-			}
-			if strings.Contains(err.Error(), "safe") {
-				t.Fatalf("protocol error leaked frame content: %v", err)
-			}
-			return err
-		}
-		time.Sleep(time.Microsecond)
-	}
-	t.Fatal("protocol violation did not become fatal")
-	return nil
+func testWebSocketAccept(key string) string {
+	sum := sha1.Sum([]byte(key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"))
+	return base64.StdEncoding.EncodeToString(sum[:])
 }
 
-func decodeGatewayFrame(t *testing.T, content []byte) Frame {
-	t.Helper()
-	var frame Frame
-	if err := json.Unmarshal(content, &frame); err != nil {
-		t.Fatal(err)
+// Only reads small masked client frames emitted by these tests.
+func readWebSocketFrame(reader *bufio.Reader) (byte, []byte, error) {
+	var header [2]byte
+	if _, err := io.ReadFull(reader, header[:]); err != nil {
+		return 0, nil, err
 	}
-	return frame
+	if header[1]&0x80 == 0 {
+		return 0, nil, errors.New("client frame is not masked")
+	}
+	length := int(header[1] & 0x7f)
+	if length == 126 {
+		var encoded [2]byte
+		if _, err := io.ReadFull(reader, encoded[:]); err != nil {
+			return 0, nil, err
+		}
+		length = int(binary.BigEndian.Uint16(encoded[:]))
+	} else if length == 127 {
+		return 0, nil, errors.New("test peer only supports small messages")
+	}
+	var mask [4]byte
+	if _, err := io.ReadFull(reader, mask[:]); err != nil {
+		return 0, nil, err
+	}
+	payload := make([]byte, length)
+	if _, err := io.ReadFull(reader, payload); err != nil {
+		return 0, nil, err
+	}
+	for i := range payload {
+		payload[i] ^= mask[i%4]
+	}
+	return header[0] & 0x0f, payload, nil
 }
 
 type heldSendTransport struct {
@@ -438,56 +522,3 @@ func (transport *heldSendTransport) Send(ctx context.Context, content []byte) er
 		return ctx.Err()
 	}
 }
-
-type discardNetConn struct{}
-
-func (discardNetConn) Read([]byte) (int, error)          { return 0, io.EOF }
-func (discardNetConn) Write(content []byte) (int, error) { return len(content), nil }
-func (discardNetConn) Close() error                      { return nil }
-func (discardNetConn) LocalAddr() net.Addr               { return discardAddr("local") }
-func (discardNetConn) RemoteAddr() net.Addr              { return discardAddr("remote") }
-func (discardNetConn) SetDeadline(time.Time) error       { return nil }
-func (discardNetConn) SetReadDeadline(time.Time) error   { return nil }
-func (discardNetConn) SetWriteDeadline(time.Time) error  { return nil }
-
-type discardAddr string
-
-func (address discardAddr) Network() string { return "discard" }
-func (address discardAddr) String() string  { return string(address) }
-
-type blockingWriteConn struct {
-	writeStarted chan struct{}
-	closed       chan struct{}
-	writeOnce    sync.Once
-	closeOnce    sync.Once
-}
-
-func newBlockingWriteConn() *blockingWriteConn {
-	return &blockingWriteConn{writeStarted: make(chan struct{}), closed: make(chan struct{})}
-}
-
-func (connection *blockingWriteConn) Read([]byte) (int, error) {
-	<-connection.closed
-	return 0, net.ErrClosed
-}
-
-func (connection *blockingWriteConn) Write([]byte) (int, error) {
-	connection.writeOnce.Do(func() { close(connection.writeStarted) })
-	<-connection.closed
-	return 0, net.ErrClosed
-}
-
-func (connection *blockingWriteConn) Close() error {
-	connection.forceClose()
-	return nil
-}
-
-func (connection *blockingWriteConn) forceClose() {
-	connection.closeOnce.Do(func() { close(connection.closed) })
-}
-
-func (*blockingWriteConn) LocalAddr() net.Addr              { return discardAddr("local") }
-func (*blockingWriteConn) RemoteAddr() net.Addr             { return discardAddr("remote") }
-func (*blockingWriteConn) SetDeadline(time.Time) error      { return nil }
-func (*blockingWriteConn) SetReadDeadline(time.Time) error  { return nil }
-func (*blockingWriteConn) SetWriteDeadline(time.Time) error { return nil }

````
