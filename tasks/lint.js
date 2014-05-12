module.exports = function(grunt) {
  grunt.registerTask("lint", ["lint:js"]);

  grunt.registerTask("lint:js", ["jshint:all"]);
};
