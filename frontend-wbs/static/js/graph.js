const DEV_API_URL = "http://localhost:5100/api";
const PROD_API_URL = "http://34.44.103.189:5100/api";
const ACTIVE_API_URL = PROD_API_URL;

const updateSummary = (query) => {
  fetch(`${ACTIVE_API_URL}/search_news/summary?${query}`, {credentials: 'include'})
  .then(res => res.json() )
  .then(json => {
    console.log(json)
    const elems = []
    json["documents"].forEach(hit => {
      let p2 = document.createElement('p');
      // p2.textContent = `Score: ${hit["score"].toFixed(2)} Magnitude: ${hit["magnitude"].toFixed(2)}`;  // Set the content of the <p> tag
      p2.textContent = `${JSON.stringify(hit)}`
      elems.push(p2);
    })
    const res_box = document.getElementById("summary-results")
    res_box.replaceChildren(...elems)
  })
  .catch(error => {
      console.error('Error fetching data:', error);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const ticker_select = document.getElementById("ticker-select")
  
  ticker_select.oninput = () => {
    updateSummary(`ticker=${ticker_select.value}`)
  }
})