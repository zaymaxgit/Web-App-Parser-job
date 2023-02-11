const express = require("express");
const { spawn } = require("child_process");
const bodyParser = require("body-parser");
const PORT = 3032;

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post("/vacancy", async (req, res) => {
  try {
    const { url } = req.body;
    if (await parse(url)) {
      const habr = require("./data/habr.json");
      const hh = require("./data/hh.json");
      res.json({ habr, hh });
    }
  } catch (error) {
    console.log(error);
  }
});

const parse = (url) => {
  return new Promise((resolve, rejects) => {
    const python = spawn("python", ["api-back/parser/parser.py", url]);
    python.stdout.on("data", (data) => {
      console.log(`Script: ${data}`);
    });
    python.stderr.on("data", (data) => {
      console.log(`Error: ${data}`);
    });
    python.on("close", (code) => {
      console.log(`Code: ${code}`);
      resolve(true);
    });
  });
};

app.listen(PORT, () => {
  console.log("Server start");
});
