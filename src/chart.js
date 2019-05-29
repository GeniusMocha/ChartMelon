const express = require("express");
const app = express();
const { PythonShell } = require("python-shell");
const mariadb = require("mariadb");

const server = app.listen(8000, checkServer);

const pool = mariadb.createPool({
  host: "localhost",
  port: 3306,
  user: "root",
  password: "",
  database: "melonchart"
});

let sendData = [];
let forEachCount = 0;

function parseFromDB() {
  // BUG: F5를 연타할 시 파이썬단 로딩이 느려 명령이 마쳐지기 전
  //      또다시 파이썬 호출이 되어버림.
  // Fixed!
  pool
    .getConnection()
    .then(function(conn) {
      conn
        .query("select * from chartmelon")
        .then(function(rows) {
          for (let i = 0; i < 100; i++) {
            sendData = rows;
          }
        })
        .then(function(res) {
          conn.end();
        })
        .catch(function(err) {
          //handle error
          console.log(err);
          conn.end();
        });
    })
    .catch(function(err) {
      //not connected
    });
  /* // 화살표 함수가 조금 낮설어서.. function으로 일단 이해하고 넘어감.
  pool
    .getConnection()
    .then(conn => {
      conn
        .query("select * from chartmelon")
        .then(rows => {
          for (let i = 0; i < 100; i++) {
            sendData = rows;
          }
        })
        .then(res => {
          conn.end();
        })
        .catch(err => {
          //handle error
          console.log(err);
          conn.end();
        });
    })
    .catch(err => {
      //not connected
    });
  */
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
}

function init() {
  PythonShell.run("parser.py", null, pyCallBack);
  app.get("/", svCallBack);
}
init();
setInterval(init, 3000);
