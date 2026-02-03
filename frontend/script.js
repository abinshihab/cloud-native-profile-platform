const apiUrl = "https://YOUR_API_ENDPOINT_HERE";

async function loadVisitorCount() {
  try {
    const response = await fetch(apiUrl);
    const count = await response.text();
    document.getElementById("visitor-count").innerText = count;
  } catch (error) {
    console.error("Failed to fetch visitor count:", error);
    document.getElementById("visitor-count").innerText = "N/A";
  }
}

document.addEventListener("DOMContentLoaded", loadVisitorCount);
