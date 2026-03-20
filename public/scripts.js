const RULES = [
  { key: "semicolonFreq", label: "Semicolons" },
  { key: "commaFreq", label: "Commas" },
  { key: "emmdashFreq", label: "Em dashes" },
  { key: "ellipsisFreq", label: "Ellipses" },
  { key: "exclamationFreq", label: "Exclamation" },
  { key: "colonFreq", label: "Colons" },
  { key: "parenthesesFreq", label: "Parentheses" },
  { key: "sentences_starter_pronouns", label: "Starts: Pronouns" },
  { key: "sentences_starter_discourse", label: "Starts: Discourse" },
  { key: "sentences_starter_and", label: "Starts: And" },
  { key: "sentences_starter_but", label: "Starts: But" },
  { key: "sentences_starter_i", label: "Starts: I" },
  { key: "sentences_starter_the", label: "Starts: The" },
  { key: "sentences_structure_avg", label: "Sentence Avg" },
  { key: "sentences_structure_variance", label: "Sentence Var" },
  { key: "sentences_structure_std_dev", label: "Sentence Std" },
  { key: "sentences_structure_long", label: "Long Sentences" },
  { key: "sentences_structure_short", label: "Short Sentences" },
  { key: "avg_para_length", label: "Paragraph Avg" },
  { key: "variance_para_length", label: "Paragraph Var" },
  { key: "std_dev_para_length", label: "Paragraph Std" },
  { key: "contraction_rate", label: "Contractions" },
  { key: "filler_word_rate", label: "Filler Words" },
  { key: "discourse_marker_rate", label: "Discourse Markers" },
  { key: "type_token_ratio", label: "Type-Token Ratio" },
  { key: "avg_word_length", label: "Word Length" },
];

const elements = {
  button: document.getElementById("go-button"),
  heatmap: document.getElementById("heatmap"),
  indexValue: document.getElementById("kevin-index-value"),
  status: document.getElementById("heatmap-status"),
  textInput: document.getElementById("text-input"),
};

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

function hashText(text) {
  let hash = 0;

  for (let index = 0; index < text.length; index += 1) {
    hash = (hash * 31 + text.charCodeAt(index)) | 0;
  }

  return Math.abs(hash);
}

function createDemoAnalysis(text) {
  const normalized = text.trim();
  const seed = hashText(normalized || "kevin-index-demo");
  const wordCount = normalized ? normalized.split(/\s+/).length : 0;
  const sentenceCount = normalized
    ? Math.max((normalized.match(/[.!?]+/g) || []).length, 1)
    : 1;
  const avgSentenceLength = wordCount / sentenceCount;
  const punctuationCount = (normalized.match(/[,:;()[\]!]/g) || []).length;
  const punctuationDensity = punctuationCount / Math.max(wordCount, 1);

  const rules = RULES.map((rule, index) => {
    const phase = seed / 97 + index * 0.71;
    const wave = Math.sin(phase) * 1.35 + Math.cos(phase / 2.3) * 0.65;
    const structureBias = (avgSentenceLength - 18) / 7;
    const punctuationBias = (punctuationDensity - 0.03) * 18;
    const signedZ = clamp(
      wave +
        structureBias * (index % 3 === 0 ? 0.5 : -0.22) +
        punctuationBias * (index % 4 === 0 ? 0.8 : -0.18),
      -3.2,
      3.2,
    );

    return {
      key: rule.key,
      label: rule.label,
      signedZ,
      direction: signedZ >= 0 ? "AI" : "human",
    };
  });

  const finalIndex = rules.reduce((total, rule) => total + rule.signedZ, 0);

  return {
    mode: "demo",
    rules,
    finalIndex,
  };
}

function normalizeRuleScore(ruleScore, index) {
  const key =
    ruleScore.key || ruleScore.rule || RULES[index]?.key || `rule_${index + 1}`;
  const fallbackLabel = RULES.find((rule) => rule.key === key)?.label || key;
  const signedZ = Number(
    ruleScore.signedZ ??
      ruleScore.signed_z ??
      ruleScore.signed_z_score ??
      ruleScore.z ??
      0,
  );

  return {
    key,
    label: ruleScore.label || ruleScore.display_name || fallbackLabel,
    signedZ: Number.isFinite(signedZ) ? signedZ : 0,
    direction: signedZ >= 0 ? "AI" : "human",
  };
}

function normalizeAnalysisPayload(payload) {
  const rawRules =
    payload.rules ||
    payload.rule_scores ||
    payload.scores ||
    payload.stats ||
    [];

  if (
    Array.isArray(rawRules) &&
    rawRules.every((value) => typeof value === "number")
  ) {
    const rules = rawRules.map((value, index) => {
      const fallbackRule = RULES[index] || {
        key: `rule_${index + 1}`,
        label: `Rule ${index + 1}`,
      };
      const signedZ = Number.isFinite(value) ? value : 0;

      return {
        key: fallbackRule.key,
        label: fallbackRule.label,
        signedZ,
        direction: signedZ >= 0 ? "AI" : "human",
      };
    });

    const rawIndex = Number(
      payload.finalIndex ?? payload.final_index ?? payload.index,
    );
    const finalIndex = Number.isFinite(rawIndex)
      ? rawIndex
      : rules.reduce((total, rule) => total + rule.signedZ, 0);

    return {
      mode: "api",
      rules,
      finalIndex,
    };
  }

  if (!Array.isArray(rawRules) || rawRules.length === 0) {
    return null;
  }

  const rules = rawRules.map(normalizeRuleScore);
  const rawIndex = Number(
    payload.finalIndex ?? payload.final_index ?? payload.index,
  );
  const finalIndex = Number.isFinite(rawIndex)
    ? rawIndex
    : rules.reduce((total, rule) => total + rule.signedZ, 0);

  return {
    mode: "api",
    rules,
    finalIndex,
  };
}

async function fetchAnalysis(text) {
  const response = await fetch("/api/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error(`Analyze request failed with status ${response.status}`);
  }

  return normalizeAnalysisPayload(await response.json());
}

function renderIndex(finalIndex) {
  const formatted = `${finalIndex >= 0 ? "+" : ""}${finalIndex.toFixed(2)}`;

  elements.indexValue.textContent = formatted;
  elements.indexValue.classList.remove("aiward", "humanward");
  elements.indexValue.classList.add(finalIndex >= 0 ? "aiward" : "humanward");
}

function renderHeatmap(analysis) {
  const scores = analysis.rules.map((rule) => rule.signedZ);
  const labels = analysis.rules.map((rule) => rule.label);
  const colorLimit = Math.max(2.5, ...scores.map((score) => Math.abs(score)));

  Plotly.react(
    elements.heatmap,
    [
      {
        type: "heatmap",
        x: labels,
        y: [""],
        z: [scores],
        zmin: -colorLimit,
        zmax: colorLimit,
        zmid: 0,
        colorscale: [
          [0, "#d95f4d"],
          [0.5, "#f4f2ef"],
          [1, "#2378c7"],
        ],
        customdata: analysis.rules.map((rule) => [rule.key, rule.direction]),
        hovertemplate:
          "<b>%{x}</b><br>" +
          "Rule: %{customdata[0]}<br>" +
          "Signed z-score: %{z:.2f}<br>" +
          "Direction: %{customdata[1]}-ward<extra></extra>",
        showscale: false,
        xgap: 2,
        ygap: 2,
      },
    ],
    {
      margin: { t: 8, r: 12, b: 92, l: 12 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      xaxis: {
        side: "bottom",
        tickangle: -42,
        tickfont: { color: "rgba(240, 244, 248, 0.86)", size: 11 },
        showgrid: false,
        zeroline: false,
        fixedrange: true,
      },
      yaxis: {
        showticklabels: false,
        showgrid: false,
        zeroline: false,
        fixedrange: true,
      },
    },
    {
      displayModeBar: false,
      responsive: true,
    },
  );

  renderIndex(analysis.finalIndex);
  elements.status.textContent =
    analysis.mode === "api"
      ? "Live data loaded from /api/calculate."
      : "Demo mode: backend unavailable, showing frontend-generated placeholder scores.";
}

async function analyzeText() {
  const text = elements.textInput.value;

  elements.button.disabled = true;
  elements.status.textContent = "Rendering heatmap...";

  try {
    const apiAnalysis = await fetchAnalysis(text);

    if (apiAnalysis) {
      renderHeatmap(apiAnalysis);
      return;
    }

    renderHeatmap(createDemoAnalysis(text));
  } catch (error) {
    renderHeatmap(createDemoAnalysis(text));
  } finally {
    elements.button.disabled = false;
  }
}

elements.button.addEventListener("click", analyzeText);
elements.textInput.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
    analyzeText();
  }
});

elements.textInput.value = [
  "This interface is rendering a frontend-only spectrogram view for grammar rules.",
  "When the backend arrives, the same component can swap from demo scores to real signed z-scores.",
].join(" ");

renderHeatmap(createDemoAnalysis(elements.textInput.value));
