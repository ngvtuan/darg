app = angular.module 'js.darg.app.options', ['js.darg.api',]

app.controller 'OptionsController', ['$scope', '$http', 'OptionPlan', 'OptionTransaction', ($scope, $http, OptionPlan, OptionTransaction) ->

    $scope.option_plans = []
    $scope.securities = []
    $scope.shareholders = []
    $scope.loading = true

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
    .finally =>
        $scope.loading = false

    $scope.add_option_plan = ->
        if $scope.newOptionPlan.board_approved_at
            $scope.newOptionPlan.board_approved_at = $scope.newOptionPlan.board_approved_at.toISOString().substring(0, 10)
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
        if $scope.newOptionTransaction.bought_at
            $scope.newOptionTransaction.bought_at = $scope.newOptionTransaction.bought_at.toISOString().substring(0, 10)
        $scope.newOptionTransaction.$save().then (result) ->
            $scope._reload_option_plans()
        .then ->
            # Reset our editor to a new blank post
            $scope.newOptionTransaction = new OptionPlan()
            $scope.show_add_option_transaction = false
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope._reload_option_plans = () ->
        $scope.option_plans = []
        $http.get('/services/rest/optionplan').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.option_plans.push item

    $scope.delete_option_transaction = (option_transaction) ->
        $http.delete('/services/rest/optiontransaction/'+option_transaction.pk).then (result) ->
            $scope._reload_option_plans()

    $scope.confirm_option_transaction = (option_transaction) ->
        $http.post('/services/rest/optiontransaction/'+option_transaction.pk+'/confirm').then (result) ->
            $scope._reload_option_plans()

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
