var gulp = require('gulp');
var path = require('path');
var concat = require('gulp-concat');
var usemin = require('gulp-usemin');
var uglify = require('gulp-uglify');
var rev = require('gulp-rev');
var minifyCss = require('gulp-minify-css');
var clean = require('gulp-clean');

var staticPath = 'static';
var htmlPath = path.join(staticPath, 'html');
var buildPath = 'build';

gulp.task('clean', function() {
  return gulp.src(buildPath, {read: false})
    .pipe(clean({force: true}));
});

gulp.task('moveHtml', ['clean', 'usemin'], function() {
  return gulp.src(path.join(buildPath, staticPath, '*.html'))
    .pipe(clean({force: true}))
    .pipe(gulp.dest(path.join(buildPath, htmlPath)));
});

gulp.task('usemin', ['clean'], function() {
  return gulp.src(path.join(htmlPath, '*.html'))
    .pipe(usemin({
      js: [uglify(), rev()],
      css: [minifyCss(), rev()]
    }))
    .pipe(gulp.dest(path.join(buildPath, staticPath)));
});

gulp.task('copyApp', ['clean'], function() {
  return gulp.src(['**/*.py', 
                   '*.yaml', 
                   path.join(staticPath, 'img', '*'),
                   path.join(staticPath, 'partials', '*.html'),
                   path.join(staticPath, 'js', '**/*.html')],
                  {base: '.'})
    .pipe(gulp.dest(buildPath));
});

gulp.task('copyYamls', ['clean'], function() {
  return gulp.src(['../queue.yaml'])
    .pipe(gulp.dest(buildPath));
});

gulp.task('buildApp', ['usemin', 'moveHtml', 'copyApp', 'copyYamls'])

gulp.task('default', ['buildApp']);