const frm = document
  .querySelector(".frm")
  .querySelector(".ui.big.relaxed.list");
const tableMax = 100;

function getChart() {
  fetch("http://localhost:8000/thisisparserapi")
    .then(response => {
      return response.json();
    })
    .then(json => {
      paintChart(json);
    });
}

function paintChart(obj) {
  for (let i = 0; i < tableMax; i++) {
    const largediv = document.createElement("div"),
      itemdiv = document.createElement("div"),
      contentdiv = document.createElement("div"),
      headerdiv = document.createElement("div");

    const img = document.createElement("img");

    largediv.setAttribute("class", "ui big relaxed list");
    itemdiv.setAttribute("class", "item");
    contentdiv.setAttribute("class", "content");
    headerdiv.setAttribute("class", "header");
    img.setAttribute("class", "ui avatar image");

    img.setAttribute("src", obj[i].img);
    const nameText = document.createTextNode(
      `${obj[i].artist} [${obj[i].album}]`
    );
    headerdiv.innerText = `${obj[i]._id}. ${obj[i].name}`;

    contentdiv.appendChild(headerdiv);
    contentdiv.appendChild(nameText);
    itemdiv.appendChild(img);
    itemdiv.appendChild(contentdiv);
    frm.append(itemdiv);
  }
}

getChart();
