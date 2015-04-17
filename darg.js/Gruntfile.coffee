module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        watch:
            coffee:
                files: ['src/javascript/**/*.coffee']
                tasks: 'coffee'
        coffee:
            files:
                src: ['src/javascript/**/*.coffee']
                dest: '../site/static/compiled/javascript/script.js'
    )
    
    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.loadNpmTasks('grunt-contrib-watch')    
    grunt.registerTask('default', ['coffee'], 'watch')
