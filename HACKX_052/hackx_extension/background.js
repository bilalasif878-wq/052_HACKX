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
    domain: tab.url ? extractDomain(tab.url) : "",
    windowId: tab.windowId // ✅ MULTI-WINDOW SUPPORT
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

  if (changeInfo.url && !changeInfo.url.startsWith("chrome://")) {
    events.push({
      ts: Date.now(),
      event: "updated",
      title: tab.title || "",
      domain: extractDomain(changeInfo.url),
      windowId: tab.windowId // ✅ MULTI-WINDOW SUPPORT
    });
    return;
  }

  if (
    changeInfo.status === "complete" &&
    tab.url &&
    !tab.url.startsWith("chrome://")
  ) {
    events.push({
      ts: Date.now(),
      event: "updated",
      title: tab.title || "",
      domain: extractDomain(tab.url),
      windowId: tab.windowId // ✅ MULTI-WINDOW SUPPORT
    });
  }
});

// --------------------
// WINDOW FOCUS LISTENER (OPTIONAL BUT IMPRESSIVE)
// --------------------
chrome.windows.onFocusChanged.addListener((windowId) => {
  if (!sessionActive || windowId === chrome.windows.WINDOW_ID_NONE) return;

  events.push({
    ts: Date.now(),
    event: "window_focus",
    windowId
  });
});

// --------------------
// POPUP MESSAGE HANDLER
// --------------------

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "START_SESSION") {
    sessionActive = true;
    startedAt = Date.now();
    endedAt = null;
    events = [];

    setTimeout(() => {
      if (sessionActive) {
        sessionActive = false;
        endedAt = Date.now();
      }
    }, MAX_SESSION_MS);

    sendResponse({ status: "started" });
    return true;
  }

  if (msg.type === "END_SESSION") {
    sessionActive = false;
    endedAt = Date.now();

    const sessionData = {
      startedAt,
      endedAt,
      durationSec: Math.round((endedAt - startedAt) / 1000),
      events
    };

    fetch("http://localhost:8000/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(sessionData)
    })
      .then(() => {
        chrome.tabs.create({
          url: "http://localhost:8501"
        });
        sendResponse({ status: "ended" });
      })
      .catch((err) => {
        console.error("Failed to send session:", err);
        sendResponse({ status: "error" });
      });

    return true; // ✅ REQUIRED FOR ASYNC
  }
});
