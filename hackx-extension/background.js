let sessionActive = false;
let startedAt = null;
let endedAt = null;
let events = [];

const MAX_SESSION_MS = 5 * 60 * 1000; // 5 minutes

// Helper to log events safely
function logEvent(type, tab) {
  if (!sessionActive || !tab) return;

  events.push({
    ts: Date.now(),
    event: type,
    title: tab.title || "",
    domain: tab.url ? extractDomain(tab.url) : ""
  });
}

// Extract domain safely
function extractDomain(url) {
  try {
    if (url.startsWith("chrome://")) return "chrome";
    return new URL(url).hostname;
  } catch {
    return "";
  }
}

// --------------------
// TAB EVENT LISTENERS
// --------------------

// Tab activated (user switches tabs)
chrome.tabs.onActivated.addListener(async (info) => {
  if (!sessionActive) return;
  const tab = await chrome.tabs.get(info.tabId);
  logEvent("activated", tab);
});

// New tab created
chrome.tabs.onCreated.addListener((tab) => {
  logEvent("created", tab);
});

// Tab closed
chrome.tabs.onRemoved.addListener((tabId) => {
  if (!sessionActive) return;
  events.push({
    ts: Date.now(),
    event: "removed",
    tabId: tabId
  });
});

// Page finished loading (CRITICAL for real domains)
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (!sessionActive) return;

  // Case 1: URL changed (SPA / redirect)
  if (changeInfo.url && !changeInfo.url.startsWith("chrome://")) {
    events.push({
      ts: Date.now(),
      event: "updated",
      title: tab.title || "",
      domain: extractDomain(changeInfo.url)
    });
    return;
  }

  // Case 2: Page finished loading (classic navigation)
  if (
    changeInfo.status === "complete" &&
    tab.url &&
    !tab.url.startsWith("chrome://")
  ) {
    events.push({
      ts: Date.now(),
      event: "updated",
      title: tab.title || "",
      domain: extractDomain(tab.url)
    });
  }
});
// --------------------
// POPUP MESSAGE HANDLER
// --------------------

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  // START SESSION
  if (msg.type === "START_SESSION") {
    sessionActive = true;
    startedAt = Date.now();
    endedAt = null;
    events = [];

    // Auto-stop after max duration
    setTimeout(() => {
      if (sessionActive) {
        sessionActive = false;
        endedAt = Date.now();
      }
    }, MAX_SESSION_MS);

    sendResponse({ status: "started" });
  }

  // END SESSION
  if (msg.type === "END_SESSION") {
    sessionActive = false;
    endedAt = Date.now();

    sendResponse({
      status: "ended",
      session: {
        startedAt,
        endedAt,
        durationSec: Math.round((endedAt - startedAt) / 1000),
        events
      }
    });
  }
});