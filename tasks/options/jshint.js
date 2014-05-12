module.exports = {
  options: {
    force: true,
    jshintrc: true,
    reporter: require("jshint-stylish")
  },
  all: [
    "flasksite/static/js/**/*.js"
  ]
};
