const startBtn = document.getElementById("startBtn");
const endBtn = document.getElementById("endBtn");
const output = document.getElementById("output");

startBtn.onclick = () => {
  chrome.runtime.sendMessage({ type: "START_SESSION" }, () => {
    output.textContent = "Session started.";
  });
};

endBtn.onclick = () => {
  chrome.runtime.sendMessage({ type: "END_SESSION" }, () => {
    output.textContent = "Session ended. Opening analysis...";
  });
};
