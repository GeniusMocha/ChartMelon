const express = require("express");
const app = express();
const { PythonShell } = require("python-shell");
const mariadb = require("mariadb");

const server = app.listen(8000, checkServer);

const pool = mariadb.createPool({
  host: "localhost",
  port: 3306,
  user: "root",
  password: "mocha00",
  database: "melonchart"
});

let sendData = [];

function parseFromDB() {
  // BUG: F5를 연타할 시 파이썬단 로딩이 느려 명령이 마쳐지기 전
  //      또다시 파이썬 호출이 되어버림.
  // Fixed! - init 내에서 미리 호출함.
  // https://mariadb.com/kb/en/library/getting-started-with-the-nodejs-connector/
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
          // 에러 감지 후 로그 찍어줌
          console.log(err);
          conn.end();
        });
    })
    .catch(err => {
      // 커넥션 실패 시 catch
      console.log(err);
    });
  /* 
    mycalled.function().getfuncfunction(function (val) {
      // Code It!
    });
    then과 같은 함수를 인자로 받는 함수(getfuncfunction)가 있을 때,
    이렇게 이해가 됨.
    mycalled.function().getfuncfunction(val => {
      // Code It!
    });

    arr.forEach(noMean => {
      // For문 돌려보기
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
setInterval(init, 36000);
