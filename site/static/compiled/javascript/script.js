(function() {
  var app;

  app = angular.module('js.darg.api', ['ngResource']);

  app.factory('Shareholder', [
    '$resource', function($resource) {
      return $resource('/services/rest/shareholders/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Company', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('User', [
    '$resource', function($resource) {
      return $resource('/services/rest/user/:id', {
        id: '@id'
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.start', ['js.darg.api']);

  app.controller('StartController', [
    '$scope', '$http', 'Company', 'Shareholder', 'User', function($scope, $http, Company, Shareholder, User) {
      $scope.shareholders = Shareholder.query().results;
      $scope.user = User.query();
      $scope.newShareholder = new Shareholder();
      $scope.add_company = function() {
        return $scope.company.$save().then(function(result) {
          return $scope.companies.push(result);
        }).then(function() {
          return $scope.company = new Company();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      return $scope.add_shareholder = function() {
        return $scope.newShareholder.$save().then(function(result) {
          return $scope.shareholders.push(result);
        }).then(function() {
          return $scope.newShareholder = new Shareholder();
        });
      };
    }
  ]);

}).call(this);
