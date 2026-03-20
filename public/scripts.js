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
  { key: "filler_word_rate", label: "Filler Words" },
  { key: "discourse_marker_rate", label: "Discourse Markers" },
  { key: "type_token_ratio", label: "Type-Token Ratio" },
  { key: "avg_word_length", label: "Word Length" },
];

const elements = {
  button: document.getElementById("go-button"),
  fileInput: document.getElementById("pdf-input"),
  fileMeta: document.getElementById("file-meta"),
  heatmap: document.getElementById("heatmap"),
  indexValue: document.getElementById("kevin-index-value"),
  status: document.getElementById("heatmap-status"),
};

pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

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
    direction: ruleScore.direction || (signedZ >= 0 ? "AI" : "human"),
    displayWeight: Number(
      ruleScore.displayWeight ?? ruleScore.display_weight ?? 1,
    ),
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
        displayWeight: 1,
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

function resetIndex() {
  elements.indexValue.textContent = "-";
  elements.indexValue.classList.remove("aiward", "humanward");
}

function formatBytes(byteCount) {
  if (!Number.isFinite(byteCount) || byteCount <= 0) {
    return "0 B";
  }

  const units = ["B", "KB", "MB", "GB"];
  const exponent = Math.min(
    Math.floor(Math.log(byteCount) / Math.log(1024)),
    units.length - 1,
  );
  const value = byteCount / 1024 ** exponent;

  return `${value.toFixed(value >= 10 || exponent === 0 ? 0 : 1)} ${units[exponent]}`;
}

function updateFileMeta(file) {
  if (!file) {
    elements.fileMeta.textContent = "No PDF selected.";
    return;
  }

  elements.fileMeta.textContent = `${file.name} • ${formatBytes(file.size)}`;
}

async function extractPdfText(file) {
  const data = new Uint8Array(await file.arrayBuffer());
  const pdf = await pdfjsLib.getDocument({ data }).promise;
  const pageTexts = [];

  for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber += 1) {
    elements.status.textContent = `Extracting text from page ${pageNumber} of ${pdf.numPages}...`;

    const page = await pdf.getPage(pageNumber);
    const textContent = await page.getTextContent();
    const text = textContent.items
      .map((item) => ("str" in item ? item.str : ""))
      .join(" ")
      .trim();

    if (text) {
      pageTexts.push(text);
    }
  }

  return pageTexts.join("\n\n").trim();
}

function clearHeatmap() {
  Plotly.purge(elements.heatmap);
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
  const weightedScores = analysis.rules.map((rule) => {
    const weight = Number.isFinite(rule.displayWeight)
      ? rule.displayWeight
      : 1.0;
    return rule.signedZ * weight;
  });
  const scoreLimit = Math.max(
    2.5,
    ...weightedScores.map((score) => Math.abs(score)),
  );
  const upperSignal = weightedScores;
  const lowerSignal = weightedScores.map((value) => -value);
  const customData = analysis.rules.map((rule, index) => [
    rule.key,
    rule.direction,
    rule.signedZ,
    weightedScores[index],
    Number.isFinite(rule.displayWeight) ? rule.displayWeight : 1.0,
  ]);

  Plotly.react(
    elements.heatmap,
    [
      {
        type: "scatter",
        x: labels,
        y: upperSignal,
        mode: "lines",
        line: {
          color: "#49a2ff",
          width: 1.5,
          shape: "spline",
          smoothing: 0.55,
        },
        customdata: customData,
        hovertemplate:
          "<b>%{x}</b><br>" +
          "Rule: %{customdata[0]}<br>" +
          "Raw z-score: %{customdata[2]:.2f}<br>" +
          "Display z-score: %{customdata[3]:.2f}<br>" +
          "Weight: %{customdata[4]:.2f}<br>" +
          "Direction: %{customdata[1]}-ward<extra></extra>",
      },
      {
        type: "scatter",
        x: labels,
        y: lowerSignal,
        mode: "lines",
        line: {
          color: "#49a2ff",
          width: 1.5,
          shape: "spline",
          smoothing: 0.55,
        },
        fill: "tonexty",
        fillcolor: "rgba(73, 162, 255, 0.78)",
        customdata: customData,
        hovertemplate:
          "<b>%{x}</b><br>" +
          "Rule: %{customdata[0]}<br>" +
          "Raw z-score: %{customdata[2]:.2f}<br>" +
          "Display z-score: %{customdata[3]:.2f}<br>" +
          "Weight: %{customdata[4]:.2f}<br>" +
          "Direction: %{customdata[1]}-ward<extra></extra>",
      },
      {
        type: "scatter",
        x: labels,
        y: labels.map(() => 0),
        mode: "lines",
        line: {
          color: "rgba(244, 242, 239, 0.58)",
          width: 1,
        },
        hoverinfo: "skip",
      },
    ],
    {
      margin: { t: 8, r: 12, b: 92, l: 56 },
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
        range: [-scoreLimit * 1.08, scoreLimit * 1.08],
        tickfont: { color: "rgba(240, 244, 248, 0.78)", size: 11 },
        showgrid: false,
        zeroline: false,
        fixedrange: true,
        title: {
          text: "Display z-score",
          font: { color: "rgba(240, 244, 248, 0.78)", size: 12 },
        },
      },
      showlegend: false,
    },
    {
      displayModeBar: false,
      responsive: true,
    },
  );

  renderIndex(analysis.finalIndex);
  elements.status.textContent = "Live data loaded from /api/calculate.";
}

async function analyzePdf() {
  const file = elements.fileInput.files?.[0];

  if (!file) {
    clearHeatmap();
    resetIndex();
    elements.status.textContent = "Choose a PDF to analyze.";
    return;
  }

  if (file.type && file.type !== "application/pdf") {
    clearHeatmap();
    resetIndex();
    elements.status.textContent = "Selected file is not a PDF.";
    return;
  }

  elements.button.disabled = true;
  elements.status.textContent = "Loading PDF...";

  try {
    const text = await extractPdfText(file);

    if (!text) {
      throw new Error("No extractable text found in the PDF.");
    }

    elements.status.textContent = "Sending extracted text to /api/calculate...";
    const apiAnalysis = await fetchAnalysis(text);

    if (!apiAnalysis) {
      throw new Error("API returned no rule scores.");
    }

    renderHeatmap(apiAnalysis);
  } catch (error) {
    clearHeatmap();
    resetIndex();
    elements.status.textContent = error.message.includes("text")
      ? "Unable to extract usable text from this PDF."
      : "Unable to analyze the PDF with /api/calculate.";
  } finally {
    elements.button.disabled = false;
  }
}

elements.button.addEventListener("click", analyzePdf);
elements.fileInput.addEventListener("change", () => {
  updateFileMeta(elements.fileInput.files?.[0] || null);
  clearHeatmap();
  resetIndex();
  elements.status.textContent = elements.fileInput.files?.[0]
    ? "PDF selected. Click Analyze PDF."
    : "Upload a PDF to analyze.";
});
