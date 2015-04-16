var gulp = require('gulp');
var path = require('path');
var concat = require('gulp-concat');
var usemin = require('gulp-usemin');
var uglify = require('gulp-uglify');
var rev = require('gulp-rev');
var minifyCss = require('gulp-minify-css');
var clean = require('gulp-clean');

var staticPath = 'static';
var templatePath = 'templates';
var buildPath = 'build';

gulp.task('clean', function() {
  return gulp.src(buildPath, {read: false})
    .pipe(clean({force: true}));
});

gulp.task('moveTemplates', ['clean', 'usemin'], function() {
  return gulp.src(path.join(buildPath, 'static', '*.template'))
    .pipe(clean({force: true}))
    .pipe(gulp.dest(path.join(buildPath, 'templates')));
})

gulp.task('usemin', ['clean'], function() {
  return gulp.src(path.join(templatePath, '*.template'))
    .pipe(usemin({
      js: [uglify(), rev()],
      css: [minifyCss(), rev()]
    }))
    .pipe(gulp.dest(path.join(buildPath, 'static')));
});

gulp.task('copyApp', ['clean'], function() {
  return gulp.src(['**/*.py', 
                   '*.yaml', 
                   path.join(staticPath, 'img', '*'),
                   path.join(staticPath, 'partials', '*.html')],
                  {base: '.'})
    .pipe(gulp.dest(buildPath));
});

gulp.task('copyYamls', ['clean'], function() {
  return gulp.src(['../queue.yaml'])
    .pipe(gulp.dest(buildPath));
});

gulp.task('buildApp', ['usemin', 'moveTemplates', 'copyApp', 'copyYamls'])

gulp.task('default', ['buildApp']);