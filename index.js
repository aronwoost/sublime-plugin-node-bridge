var util = require("util");

var input = JSON.parse(process.argv[2]);
console.log("input from sublime plugin was: " + util.inspect(input));
