const gulp = require('gulp');
const ghPages = require('gh-pages');
const { exec } = require('child_process');
const path = require('path');

gulp.task('build', function (cb) {
    exec('gitbook build', function (err, stdout, stderr) {
        console.log(stdout);
        console.log(stderr);
        cb(err);
    });
});

gulp.task('deploy', function (cb) {
    ghPages.publish(path.join(__dirname, '_book'), cb);
});

gulp.task('default', gulp.series('build', 'deploy'));