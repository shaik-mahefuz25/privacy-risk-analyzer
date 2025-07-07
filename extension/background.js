chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyzePII",
    title: "🔍 Analyze Privacy Risks",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyzePII") {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: analyzeSelectedText,
    });
  }
});

function analyzeSelectedText() {
  const selectedText = window.getSelection().toString();
  if (selectedText) {
    const url = `http://localhost:8501/?q=${encodeURIComponent(selectedText)}`

    window.open(url, "_blank");
  } else {
    alert("No text selected.");
  }
}
