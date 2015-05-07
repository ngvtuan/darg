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

  app.factory('Position', [
    '$resource', function($resource) {
      return $resource('/services/rest/position/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Invitee', [
    '$resource', function($resource) {
      return $resource('/services/rest/invitee/:id', {
        id: '@id'
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.base', ['js.darg.api']);

  app.controller('BaseController', [
    '$scope', '$http', function($scope, $http) {
      return this.scope.test = True;
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.index', ['js.darg.api']);

  app.controller('IndexController', [
    '$scope', '$http', 'Invitee', function($scope, $http, Invitee) {
      $scope.show_add_invitee = true;
      $scope.newInvitee = new Invitee();
      $scope.errors = [];
      return $scope.add_invitee = function() {
        return $scope.newInvitee.$save().then(function(result) {
          $scope.show_add_invitee = false;
          if (!_.isUndefined(window.ga)) {
            return ga('send', 'event', 'click', 'save_invitee_email');
          }
        }).then(function() {
          return $scope.newInvitee = new Invitee();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.positions', ['js.darg.api']);

  app.controller('PositionsController', [
    '$scope', '$http', 'Position', function($scope, $http, Position) {
      $scope.positions = [];
      $scope.show_add_position = false;
      $scope.newPosition = new Position();
      $http.get('/services/rest/position').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.positions.push(item);
        });
      });
      return $scope.add_position = function() {
        return $scope.newPosition.$save().then(function(result) {
          return $scope.positions.push(result);
        }).then(function() {
          return $scope.newPosition = new Position();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.shareholder', ['js.darg.api']);

  app.controller('ShareholderController', [
    '$scope', '$http', function($scope, $http) {
      return $scope.test = true;
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.start', ['js.darg.api']);

  app.controller('StartController', [
    '$scope', '$http', 'Company', 'Shareholder', 'User', function($scope, $http, Company, Shareholder, User) {
      $scope.shareholders = [];
      $scope.user = [];
      $scope.newShareholder = new Shareholder();
      $scope.newCompany = new Company();
      $http.get('/services/rest/shareholders').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.shareholders.push(item);
        });
      });
      $http.get('/services/rest/user').then(function(result) {
        return $scope.user = result.data.results[0];
      });
      $scope.add_company = function() {
        return $scope.newCompany.$save().then(function(result) {
          return $http.get('/services/rest/user').then(function(result) {
            $scope.user = result.data.results[0];
            return console.log($scope.user);
          });
        }).then(function() {
          return $scope.company = new Company();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      $scope.add_shareholder = function() {
        return $scope.newShareholder.$save().then(function(result) {
          return $scope.shareholders.push(result);
        }).then(function() {
          return $scope.newShareholder = new Shareholder();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      return $scope.goto_shareholder = function(shareholder_id) {
        return window.location = "/shareholder/" + shareholder_id + "/";
      };
    }
  ]);

}).call(this);

(function() {
  $('.table tr').each(function() {
    $(this).css('cursor', 'pointer').hover((function() {
      $(this).addClass('active');
    }), function() {
      $(this).removeClass('active');
    });
  });

  return;

}).call(this);
