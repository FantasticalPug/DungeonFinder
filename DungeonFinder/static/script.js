if ("serviceWorker" in navigator) {
  window.addEventListener('load', () => {
    this.navigator.serviceWorker.register('/service-worker.js', {
		  scope: '/'
	  });
  });
}

function when18() {
  var date = new Date();
  date.setFullYear(date.getFullYear() - 18);
  var year = date.getFullYear();
  var month = date.getMonth() + 1;
  var day = date.getDate();
  if (day < 10) {
    day = "0" + day;
  }
  if (month < 10) {
    month = "0" + month;
  }
  adult = year + "-" + month + "-" + day;
  document.getElementById("DoB").setAttribute("max", adult);
}

window.addEventListener("load", () => {
  if (document.getElementById("DoB") !== null) {
    when18();
  }
});
