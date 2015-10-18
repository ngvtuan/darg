app = angular.module 'js.darg.app.options', ['js.darg.api',]

app.controller 'OptionsController', ['$scope', '$http', 'OptionPlan', 'OptionTransaction', ($scope, $http, OptionPlan, OptionTransaction) ->

    $scope.option_plans = []
    $scope.securities = []
    $scope.shareholders = []

    $scope.show_add_option_transaction = false
    $scope.show_add_option_plan = false
    $scope.newOptionPlan = new OptionPlan()

    $http.get('/services/rest/optionplan').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.option_plans.push item

    $http.get('/services/rest/security').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.securities.push item

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.shareholders.push item 

    $scope.add_option_plan = ->
        $scope.newOptionPlan.$save().then (result) ->
            $scope.option_plans.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.newOptionPlan = new OptionPlan()
            $scope.show_add_option_plan = false
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.add_option_transaction = ->
        $scope.newOptionTransaction.$save().then (result) ->
            # $scope.option_plans.push result
            # FIXME and replace with proper push to $scope.option_plans
            $scope.option_plans = []
            $http.get('/services/rest/optionplan').then (result) ->
                angular.forEach result.data.results, (item) ->
                    $scope.option_plans.push item
        .then ->
            # Reset our editor to a new blank post
            $scope.newOptionTransaction = new OptionPlan()
            $scope.show_add_option_transaction = false
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.show_add_option_plan_form = ->
        $scope.show_add_option_plan = true
        $scope.show_add_option_transaction = false
        $scope.newOptionPlan = new OptionPlan()

    $scope.show_add_option_transaction_form = ->
        $scope.show_add_option_transaction = true
        $scope.show_add_option_plan = false
        $scope.newOptionTransaction = new OptionTransaction()

    $scope.hide_form = ->
        $scope.show_add_option_plan = false
        $scope.show_add_option_transaction = false
        $scope.newOptionPlan = new OptionPlan()
        $scope.newOptionTransaction = new OptionTransaction()

]
