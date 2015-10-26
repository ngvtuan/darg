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

  app.factory('CompanyAdd', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/add/');
    }
  ]);

  app.factory('Company', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('Country', [
    '$resource', function($resource) {
      return $resource('/services/rest/country/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
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

  app.factory('OptionPlan', [
    '$resource', function($resource) {
      return $resource('/services/rest/optionplan/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('OptionTransaction', [
    '$resource', function($resource) {
      return $resource('/services/rest/optiontransaction/:id', {
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

  app = angular.module('js.darg.app.company', ['js.darg.api', 'xeditable']);

  app.controller('CompanyController', [
    '$scope', '$http', 'Company', 'Country', function($scope, $http, Company, Country) {
      $http.get('/services/rest/company/' + company_id).then(function(result) {
        $scope.company = new Company(result.data);
        return $http.get($scope.company.country).then(function(result1) {
          return $scope.company.country = result1.data;
        });
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      return $scope.edit_company = function() {
        $scope.company.country = $scope.company.country.url;
        return $scope.company.$update().then(function(result) {
          $scope.company = new Company(result);
          $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
          return console.log($scope.company);
        }).then(function() {
          return void 0;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

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

  app = angular.module('js.darg.app.options', ['js.darg.api']);

  app.controller('OptionsController', [
    '$scope', '$http', 'OptionPlan', 'OptionTransaction', function($scope, $http, OptionPlan, OptionTransaction) {
      $scope.option_plans = [];
      $scope.securities = [];
      $scope.shareholders = [];
      $scope.show_add_option_transaction = false;
      $scope.show_add_option_plan = false;
      $scope.newOptionPlan = new OptionPlan();
      $http.get('/services/rest/optionplan').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.option_plans.push(item);
        });
      });
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $http.get('/services/rest/shareholders').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.shareholders.push(item);
        });
      });
      $scope.add_option_plan = function() {
        return $scope.newOptionPlan.$save().then(function(result) {
          return $scope.option_plans.push(result);
        }).then(function() {
          $scope.newOptionPlan = new OptionPlan();
          return $scope.show_add_option_plan = false;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      $scope.add_option_transaction = function() {
        return $scope.newOptionTransaction.$save().then(function(result) {
          $scope.option_plans = [];
          return $http.get('/services/rest/optionplan').then(function(result) {
            return angular.forEach(result.data.results, function(item) {
              return $scope.option_plans.push(item);
            });
          });
        }).then(function() {
          $scope.newOptionTransaction = new OptionPlan();
          return $scope.show_add_option_transaction = false;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      $scope.show_add_option_plan_form = function() {
        $scope.show_add_option_plan = true;
        $scope.show_add_option_transaction = false;
        return $scope.newOptionPlan = new OptionPlan();
      };
      $scope.show_add_option_transaction_form = function() {
        $scope.show_add_option_transaction = true;
        $scope.show_add_option_plan = false;
        return $scope.newOptionTransaction = new OptionTransaction();
      };
      return $scope.hide_form = function() {
        $scope.show_add_option_plan = false;
        $scope.show_add_option_transaction = false;
        $scope.newOptionPlan = new OptionPlan();
        return $scope.newOptionTransaction = new OptionTransaction();
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.optionplan', ['js.darg.api', 'xeditable']);

  app.controller('OptionPlanController', [
    '$scope', '$http', 'OptionPlan', function($scope, $http, OptionPlan) {
      $http.get('/services/rest/optionplan/' + optionplan_id).then(function(result) {
        $scope.optionplan = new OptionPlan(result.data);
        return $http.get($scope.optionplan.security).then(function(result1) {
          return $scope.optionplan.security = result1.data;
        });
      });
      $http.get('/services/rest/security').then(function(result) {
        return $scope.securities = result.data.results;
      });
      return $scope.edit_company = function() {
        $scope.company.country = $scope.company.country.url;
        return $scope.company.$update().then(function(result) {
          $scope.company = new Company(result);
          $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
          return console.log($scope.company);
        }).then(function() {
          return void 0;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.positions', ['js.darg.api']);

  app.controller('PositionsController', [
    '$scope', '$http', 'Position', function($scope, $http, Position) {
      $scope.positions = [];
      $scope.shareholders = [];
      $scope.securities = [];
      $scope.show_add_position = false;
      $scope.show_add_capital = false;
      $scope.newPosition = new Position();
      $http.get('/services/rest/position').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.positions.push(item);
        });
      });
      $http.get('/services/rest/shareholders').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.shareholders.push(item);
        });
      });
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $scope.add_position = function() {
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
      $scope.show_add_position_form = function() {
        $scope.show_add_position = true;
        $scope.show_add_capital = false;
        return $scope.newPosition = new Position();
      };
      $scope.show_add_capital_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = true;
        return $scope.newPosition = new Position();
      };
      return $scope.hide_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        return $scope.newPosition = new Position();
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
    '$scope', '$http', 'CompanyAdd', 'Shareholder', 'User', function($scope, $http, CompanyAdd, Shareholder, User) {
      $scope.shareholders = [];
      $scope.user = [];
      $scope.show_add_shareholder = false;
      $scope.newShareholder = new Shareholder();
      $scope.newCompany = new CompanyAdd();
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
      $scope.show_add_shareholder_form = function() {
        return $scope.show_add_shareholder = true;
      };
      $scope.hide_form = function() {
        return $scope.show_add_shareholder = false;
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
