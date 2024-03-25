document.getElementById("dataForm").addEventListener("submit", function(event) {
  event.preventDefault();
  var startDate = document.getElementById("startDate").value;
  var endDate = document.getElementById("endDate").value;
  var isins = document.getElementById("isin").value.split(",").map(item => item.trim());
  // Perform further processing here (e.g., send data to server)
  console.log("Start Date:", startDate);
  console.log("End Date:", endDate);
  console.log("ISINs:", isins);
});
