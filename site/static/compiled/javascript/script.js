(function() {
  var app;

  app = angular.module('js.darg.api', ['ngResource']);

  app.factory('Shareholder', [
    '$resource', function($resource) {
      return $resource('/services/rest/shareholders/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
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

  app.factory('Split', [
    '$resource', function($resource) {
      return $resource('/services/rest/split/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Operator', [
    '$resource', function($resource) {
      return $resource('/services/rest/operators/:id', {
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
    '$scope', '$http', 'Company', 'Country', 'Operator', function($scope, $http, Company, Country, Operator) {
      $scope.operators = [];
      $scope.company = null;
      $scope.errors = null;
      $scope.show_add_operator_form = false;
      $scope.newOperator = new Operator();
      $http.get('/services/rest/company/' + company_id).then(function(result) {
        $scope.company = new Company(result.data);
        $scope.company.founded_at = new Date($scope.company.founded_at);
        return $http.get($scope.company.country).then(function(result1) {
          return $scope.company.country = result1.data;
        });
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      $http.get('/services/rest/operators').then(function(result) {
        return $scope.operators = result.data.results;
      });
      $scope.toggle_add_operator_form = function() {
        if ($scope.show_add_operator_form) {
          return $scope.show_add_operator_form = false;
        } else {
          return $scope.show_add_operator_form = true;
        }
      };
      $scope.delete_operator = function(pk) {
        return $http["delete"]('/services/rest/operators/' + pk).then(function() {
          return $http.get('/services/rest/operators').then(function(result) {
            return $scope.operators = result.data.results;
          });
        });
      };
      $scope.add_operator = function() {
        $scope.newOperator.company = $scope.company.url;
        return $scope.newOperator.$save().then(function(result) {
          return $http.get('/services/rest/operators').then(function(result) {
            return $scope.operators = result.data.results;
          });
        }).then(function() {
          return $scope.newOperator = new Operator();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      return $scope.edit_company = function() {
        if ($scope.company.country) {
          $scope.company.country = $scope.company.country.url;
        }
        $scope.company.founded_at = $scope.company.founded_at.toISOString().substring(0, 10);
        return $scope.company.$update().then(function(result) {
          result.founded_at = new Date(result.founded_at);
          $scope.company = new Company(result);
          return $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
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
        if ($scope.newOptionPlan.board_approved_at) {
          $scope.newOptionPlan.board_approved_at = $scope.newOptionPlan.board_approved_at.toISOString().substring(0, 10);
        }
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
        if ($scope.newOptionTransaction.bought_at) {
          $scope.newOptionTransaction.bought_at = $scope.newOptionTransaction.bought_at.toISOString().substring(0, 10);
        }
        return $scope.newOptionTransaction.$save().then(function(result) {
          return $scope._reload_option_plans();
        }).then(function() {
          $scope.newOptionTransaction = new OptionPlan();
          return $scope.show_add_option_transaction = false;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      $scope._reload_option_plans = function() {
        $scope.option_plans = [];
        return $http.get('/services/rest/optionplan').then(function(result) {
          return angular.forEach(result.data.results, function(item) {
            return $scope.option_plans.push(item);
          });
        });
      };
      $scope.delete_option_transaction = function(option_transaction) {
        return $http["delete"]('/services/rest/optiontransaction/' + option_transaction.pk).then(function(result) {
          return $scope._reload_option_plans();
        });
      };
      $scope.confirm_option_transaction = function(option_transaction) {
        return $http.post('/services/rest/optiontransaction/' + option_transaction.pk + '/confirm').then(function(result) {
          return $scope._reload_option_plans();
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

  app = angular.module('js.darg.app.optionplan', ['js.darg.api', 'xeditable', 'ngFileUpload']);

  app.controller('OptionPlanController', [
    '$scope', '$http', 'OptionPlan', 'Upload', '$timeout', function($scope, $http, OptionPlan, Upload, $timeout) {
      $scope.file = null;
      $scope.pdf_upload_success = false;
      $scope.pdf_upload_errors = false;
      $http.get('/services/rest/optionplan/' + optionplan_id).then(function(result) {
        $scope.optionplan = new OptionPlan(result.data);
        return $scope.optionplan.board_approved_at = $scope.optionplan.board_approved_at;
      });
      $http.get('/services/rest/security').then(function(result) {
        return $scope.securities = result.data.results;
      });
      $scope.$watch('files', function() {
        $scope.upload($scope.files);
      });
      $scope.$watch('file', function() {
        if ($scope.file !== null) {
          $scope.files = [$scope.file];
        }
      });
      $scope.log = '';
      return $scope.upload = function(files) {
        var file, i, payload;
        if (files && files.length) {
          i = 0;
          while (i < files.length) {
            file = files[i];
            if (!file.$error) {
              payload = $scope.optionplan;
              payload.pdf_file = file;
              Upload.upload({
                url: '/services/rest/optionplan/' + optionplan_id + '/upload',
                data: payload,
                objectKey: '.k'
              }).then((function(response) {
                $timeout(function() {
                  $scope.optionplan = response.data;
                  $scope.pdf_upload_success = true;
                  $scope.pdf_upload_errors = false;
                });
                return $timeout(function() {
                  return $scope.pdf_upload_success = false;
                }, 3000);
              }), (function(response) {
                return $timeout(function() {
                  return $scope.pdf_upload_errors = response.data;
                });
              }), function(evt) {});
              return;
            }
          }
        }
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
    '$scope', '$http', 'Position', 'Split', function($scope, $http, Position, Split) {
      $scope.positions = [];
      $scope.shareholders = [];
      $scope.securities = [];
      $scope.show_add_position = false;
      $scope.show_add_capital = false;
      $scope.show_split_data = false;
      $scope.show_split = false;
      $scope.newPosition = new Position();
      $scope.newSplit = new Split();
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
        if ($scope.newPosition.bought_at) {
          $scope.newPosition.bought_at = $scope.newPosition.bought_at.toISOString().substring(0, 10);
        }
        return $scope.newPosition.$save().then(function(result) {
          return $scope.positions.push(result);
        }).then(function() {
          $scope.show_add_position = false;
          $scope.show_add_capital = false;
          return $scope.newPosition = new Position();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      $scope.delete_position = function(position) {
        return $http["delete"]('/services/rest/position/' + position.pk).then(function(result) {
          $scope.positions = [];
          return $http.get('/services/rest/position').then(function(result1) {
            return angular.forEach(result1.data.results, function(item) {
              return $scope.positions.push(item);
            });
          });
        });
      };
      $scope.confirm_position = function(position) {
        return $http.post('/services/rest/position/' + position.pk + '/confirm').then(function(result) {
          $scope.positions = [];
          return $http.get('/services/rest/position').then(function(result1) {
            return angular.forEach(result1.data.results, function(item) {
              return $scope.positions.push(item);
            });
          });
        });
      };
      $scope.add_split = function() {
        return $scope.newSplit.$save().then(function(result) {
          return $scope.positions = result.data;
        }).then(function() {
          return $scope.newSplit = new Split();
        }).then(function() {
          $scope.errors = null;
          return $scope.show_split = false;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
      $scope.show_add_position_form = function() {
        $scope.show_add_position = true;
        $scope.show_add_capital = false;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.toggle_show_split_data = function() {
        if ($scope.show_split_data) {
          return $scope.show_split_data = false;
        } else {
          return $scope.show_split_data = true;
        }
      };
      $scope.show_add_capital_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = true;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.hide_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      return $scope.show_split_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        $scope.newSplit = new Split();
        return $scope.show_split = true;
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.shareholder', ['js.darg.api', 'xeditable']);

  app.controller('ShareholderController', [
    '$scope', '$http', 'Shareholder', function($scope, $http, Shareholder) {
      $scope.shareholder = true;
      $scope.errors = null;
      $http.get('/services/rest/shareholders/' + shareholder_id).then(function(result) {
        result.data.user.userprofile.birthday = new Date(result.data.user.userprofile.birthday);
        $scope.shareholder = new Shareholder(result.data);
        return $http.get($scope.shareholder.user.userprofile.country).then(function(result1) {
          return $scope.shareholder.user.userprofile.country = result1.data;
        });
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      return $scope.edit_shareholder = function() {
        if ($scope.shareholder.user.userprofile.country) {
          $scope.shareholder.user.userprofile.country = $scope.shareholder.user.userprofile.country.url;
        }
        if ($scope.shareholder.user.userprofile.birthday) {
          $scope.shareholder.user.userprofile.birthday = $scope.shareholder.user.userprofile.birthday.toISOString().substring(0, 10);
        }
        return $scope.shareholder.$update().then(function(result) {
          result.user.userprofile.birthday = new Date(result.user.userprofile.birthday);
          $scope.shareholder = new Shareholder(result);
          return $http.get($scope.shareholder.user.userprofile.country).then(function(result1) {
            return $scope.shareholder.user.userprofile.country = result1.data;
          });
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

  app = angular.module('js.darg.app.start', ['js.darg.api']);

  app.controller('StartController', [
    '$scope', '$http', 'CompanyAdd', 'Shareholder', 'User', 'Company', function($scope, $http, CompanyAdd, Shareholder, User, Company) {
      $scope.shareholders = [];
      $scope.user = [];
      $scope.total_shares = 0;
      $scope.show_add_shareholder = false;
      $scope.newShareholder = new Shareholder();
      $scope.newCompany = new CompanyAdd();
      $http.get('/services/rest/shareholders').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.shareholders.push(item);
        });
      });
      $http.get('/services/rest/user').then(function(result) {
        $scope.user = result.data.results[0];
        return angular.forEach($scope.user.operator_set, function(item, key) {
          return $http.get(item.company).then(function(result1) {
            return $scope.user.operator_set[key].company = result1.data;
          });
        });
      });
      $scope.$watchCollection('shareholders', function(shareholders) {
        $scope.total_shares = 0;
        return angular.forEach(shareholders, function(item) {
          return $scope.total_shares = item.share_count + $scope.total_shares;
        });
      });
      $scope.add_company = function() {
        if ($scope.newCompany.founded_at) {
          $scope.newCompany.founded_at = $scope.newCompany.founded_at.toISOString().substring(0, 10);
        } else {
          delete $scope.newCompany.founded_at;
        }
        return $scope.newCompany.$save().then(function(result) {
          $http.get('/services/rest/user').then(function(result) {
            $scope.user = result.data.results[0];
            return angular.forEach($scope.user.operator_set, function(item, key) {
              return $http.get(item.company).then(function(result1) {
                return $scope.user.operator_set[key].company = result1.data;
              });
            });
          });
          return $http.get('/services/rest/shareholders').then(function(result) {
            return angular.forEach(result.data.results, function(item) {
              return $scope.shareholders.push(item);
            });
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
