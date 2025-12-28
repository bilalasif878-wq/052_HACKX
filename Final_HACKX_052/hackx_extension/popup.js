const startBtn = document.getElementById("startBtn");
const endBtn = document.getElementById("endBtn");
const status = document.getElementById("status");

startBtn.onclick = () => {
  chrome.runtime.sendMessage({ type: "START_SESSION" }, () => {
    status.textContent = "Session started.";
  });
};

endBtn.onclick = () => {
  chrome.runtime.sendMessage({ type: "END_SESSION" }, () => {
    status.textContent = "Session ended. Opening analysis...";
  });
};
