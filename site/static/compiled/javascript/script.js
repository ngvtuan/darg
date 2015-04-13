(function() {
  var app;

  app = angular.module('js.darg.app.static', []);

  app.controller('AppController', [
    '$scope', '$http', function($scope, $http) {
      $scope.shareholders = [];
      return $http.get('/services/rest/shareholders/').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.shareholders.push(item);
        });
      });
    }
  ]);

}).call(this);
