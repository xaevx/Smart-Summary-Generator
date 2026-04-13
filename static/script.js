document.getElementById("summaryForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const formData = new FormData(e.target);

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "⏳ Generating summary...";

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    resultDiv.innerHTML = result.summary;
  } catch (error) {
    resultDiv.innerHTML = "❌ Error: Unable to generate summary.";
    console.error("Fetch error:", error);
  }
});
