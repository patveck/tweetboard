module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON("package.json"),
        jshint: {
            files: ["Gruntfile.js", "js/**/*.js", "tests/jasmine-specs/*.js"],
            options: {
                camelcase: true,
                immed: true,
                latedef: true,
                newcap: true,
                nonew: true,
                quotmark: true,
                trailing: true,
                maxparams: 5,
                maxstatements: 50,
                maxdepth: 4,
                maxlen: 80
            }
        },
        watch: {
            files: ["<%= jshint.files %>"],
            tasks : ["jshint", "qunit"]
        },
        karma: {
            unit: {
              configFile: "karma.conf.js",
              singleRun: true,
              browsers: ["PhantomJS"]
            }
        },
        jsdoc: {
            dist: {
                src: ["js/**/*.js", "tests/jasmine-specs/*.js",
                      "doc/client/jsdoc.md"],
                options: {
                    configure: "doc/client/jsdoc_conf.json",
                    destination: "doc/client"
                }
            }
        }
    });

    grunt.loadNpmTasks("grunt-contrib-jshint");
    grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks("grunt-karma");
    grunt.loadNpmTasks("grunt-jsdoc");

    grunt.registerTask("test", ["jshint"]);

    grunt.registerTask("default", ["jshint", "karma", "jsdoc"]);

};
