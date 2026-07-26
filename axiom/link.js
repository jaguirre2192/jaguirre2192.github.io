const kind = window.location.pathname.includes("/reply/") ? "reply" : "invite";
const query = window.location.search;
const openButton = document.querySelector("#open-in-axiom");
const storeButton = document.querySelector("#app-store");
const storeStatus = document.querySelector("#store-status");

openButton.href = `axiom://${kind}${query}`;

fetch("https://itunes.apple.com/lookup?bundleId=com.jorgeaguirre.Axiom&country=us")
  .then((response) => response.ok ? response.json() : Promise.reject())
  .then((payload) => {
    const app = payload.results?.[0];
    if (!app?.trackViewUrl) {
      storeStatus.textContent = "Axiom is not currently listed on the App Store.";
      return;
    }

    storeButton.href = app.trackViewUrl;
    storeButton.hidden = false;
    storeStatus.textContent = "If Axiom is not installed, download it from the App Store.";
  })
  .catch(() => {
    storeStatus.textContent = "App Store availability could not be checked right now.";
  });
