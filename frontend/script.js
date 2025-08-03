async function search() {
  const query = document.getElementById("query").value;
  const response = await fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(query)}`);
  const data = await response.json();

  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  data.forEach(article => {
    const div = document.createElement("div");
    div.className = "article";
    div.innerHTML = `<h3>${article.title}</h3>
                     <p><strong>Score:</strong> ${article.score.toFixed(2)}</p>
                     <p>${article.content}</p>`;
    resultsDiv.appendChild(div);
  });
}
