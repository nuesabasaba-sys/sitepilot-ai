const form = document.getElementById("analyzeForm");
const urlInput = document.getElementById("urlInput");
const analyzeButton = document.getElementById("analyzeButton");
const buttonLabel = analyzeButton.querySelector(".button-label");
const statusMessage = document.getElementById("statusMessage");
const errorMessage = document.getElementById("errorMessage");
const results = document.getElementById("results");

const categories = [
  { key: "seo", title: "SEO" },
  { key: "copywriting", title: "コピーライティング" },
  { key: "cta", title: "CTA" },
  { key: "readability", title: "読みやすさ" },
];

function makeListGroup(label, items, isSuggestion = false) {
  const group = document.createElement("div");
  group.className = "list-group";

  const heading = document.createElement("p");
  heading.className = `list-label${isSuggestion ? " suggestion-label" : ""}`;
  heading.textContent = label;
  group.append(heading);

  const list = document.createElement("ul");
  list.className = `bullet-list${isSuggestion ? " suggestion-list" : ""}`;
  const entries = Array.isArray(items) && items.length > 0 ? items : ["該当なし"];

  for (const item of entries) {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    if (item === "該当なし") listItem.className = "empty-item";
    list.append(listItem);
  }

  group.append(list);
  return group;
}

function renderAnalysis(data) {
  for (const category of categories) {
    const card = document.querySelector(`[data-category="${category.key}"]`);
    const content = card.querySelector(".card-content");
    const section = data[category.key] || {};

    content.replaceChildren(
      makeListGroup("問題点", section.issues),
      makeListGroup("改善案", section.suggestions, true),
    );
  }

  document.getElementById("targetAudience").textContent = data.target_audience || "記載がありません。";
  const overallIssues = document.getElementById("overallIssues");
  overallIssues.replaceWith(makeListGroup("", data.overall_issues).querySelector("ul"));
  const updatedIssues = document.querySelector(".issues-card .bullet-list");
  updatedIssues.id = "overallIssues";

  document.getElementById("titleSuggestion").textContent = data.title_suggestion || "記載がありません。";
  document.getElementById("metaSuggestion").textContent = data.meta_description_suggestion || "記載がありません。";
  document.getElementById("h1Suggestion").textContent = data.h1_suggestion || "記載がありません。";
  results.hidden = false;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;

  errorMessage.hidden = true;
  errorMessage.textContent = "";
  results.hidden = true;
  statusMessage.textContent = "分析中... ページの内容を確認しています。";
  statusMessage.hidden = false;
  analyzeButton.disabled = true;
  analyzeButton.setAttribute("aria-busy", "true");
  buttonLabel.textContent = "分析中...";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput.value.trim() }),
    });

    if (!response.ok) throw new Error("分析リクエストに失敗しました。");
    const data = await response.json();
    renderAnalysis(data);
    statusMessage.textContent = "分析が完了しました。";
  } catch (error) {
    errorMessage.textContent = "分析に失敗しました。URLを確認して、もう一度お試しください。";
    errorMessage.hidden = false;
    statusMessage.textContent = "";
    statusMessage.hidden = true;
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.removeAttribute("aria-busy");
    buttonLabel.textContent = "分析する";
  }
});
