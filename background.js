let bannedDomains = [];
let bannedKeywords = [];

fetch(chrome.runtime.getURL("banned_domains.json"))
  .then(res => res.json())
  .then(data => { bannedDomains = data; });

fetch(chrome.runtime.getURL("banned_keywords.json"))
  .then(res => res.json())
  .then(data => { bannedKeywords = data; });

chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    const url = details.url.toLowerCase();

    for (let domain of bannedDomains) {
      if (url.includes(domain)) {
        console.log("Blocked domain:", url);
        return { cancel: true };
      }
    }

    for (let keyword of bannedKeywords) {
      if (url.includes(keyword)) {
        console.log("Blocked keyword:", url);
        return { cancel: true };
      }
    }

    return { cancel: false };
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);