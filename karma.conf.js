// Karma configuration
// Generated on Tue Jun 18 2013 23:58:25 GMT+0200 (W. Europe Daylight Time)


// base path, that will be used to resolve files and exclude
basePath = '';


// list of files / patterns to load in the browser
files = [
  JASMINE,
  JASMINE_ADAPTER,
  REQUIRE,
  REQUIRE_ADAPTER,

  {pattern: 'lib/**/*.js', included: false},
  {pattern: 'js/**/*.js', included: false},
  {pattern: 'tests/jasmine-specs/*Spec.js', included: false},

  'tests/jasmine-specs/test-main.js'
];

preprocessors = {
    'js/*.js': 'coverage'
};


// list of files to exclude
exclude = [
    'js/main.js'
];


// test results reporter to use
// possible values: 'dots', 'progress', 'junit'
reporters = ['progress', 'coverage'];

coverageReporter = {
    type : 'lcov',
    dir : 'coverage/client'
};

// web server port
port = 9876;


// cli runner port
runnerPort = 9100;


// enable / disable colors in the output (reporters and logs)
colors = true;


// level of logging
// possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || 
//                  LOG_INFO || LOG_DEBUG
logLevel = LOG_INFO;


// enable / disable watching file and executing tests whenever any file changes
autoWatch = true;


// Start these browsers, currently available:
// - Chrome
// - ChromeCanary
// - Firefox
// - Opera
// - Safari (only Mac)
// - PhantomJS
// - IE (only Windows)
browsers = ['PhantomJS'];


// If browser does not capture in given timeout [ms], kill it
captureTimeout = 60000;


// Continuous Integration mode
// if true, it capture browsers, run tests and exit
singleRun = false;
