module.exports = function(grunt) {
    
    // Configure plugins.
    grunt.initConfig({
        
        // grunt-contrib-jshint
        jshint: {
            src: [
                "./Gruntfile.js",
                "./static/**/*.js"
            ]
        }
    });
    
    // Load plugins.
    grunt.loadNpmTasks("grunt-contrib-jshint");
    
    // Register tasks.
    grunt.registerTask("default", "jshint");
};
