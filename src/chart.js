const express = require("express");
const app = express();
const fs = require("fs");
const cors = require("cors");
const { PythonShell } = require("python-shell");
const path = require("path");
const { Pool } = require("pg");

const pool = new Pool({
  host: "localhost",
  port: 5432,
  user: "postgres",
  password: "mocha00",
  database: "postgres"
});

const port = 8000;
const server = app.listen(port, checkServer);

let sendData = [];

function parseFromDB() {
  // BUG: F5를 연타할 시 파이썬단 로딩이 느려 명령이 마쳐지기 전
  //      또다시 파이썬 호출이 되어버림.
  // Fixed! - init 내에서 미리 호출함.
  // https://node-postgres.com/api/pool
  pool.connect((err, client, release) => {
    if (err) {
      return console.error("Error!", err.stack);
    }

    client.query("ALTER DATABASE melonchart");

    client.query("SELECT * FROM chartmelon", (err, result) => {
      release();
      if (err) {
        return console.error("Error!", err.stack);
      }
      sendData = result.rows;
    });
  });
}

function pyCallBack(err, stdout) {
  if (err) throw err;
  parseFromDB();
}

function svCallBack(req, res) {
  res.send(sendData);
}

function checkServer() {
  console.log("서버가 성공적으로 작동되고 있습니다.");
  console.log(`Port : ${port}`);
}

function init() {
  PythonShell.run("parser.py", null, pyCallBack);

  app.use(express.static(path.join(__dirname, "/")));
  app.use(cors());

  app.get("/thisisparserapi", svCallBack);
  app.get("/", (req, res) => {
    fs.readFile("index.html", (error, data) => {
      res.writeHead(200, {
        "Content-Type": "text/html"
      });
      res.end(data);
    });
  });
}
init();
setInterval(init, 3600000);
