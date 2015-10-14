app = angular.module 'js.darg.app.optionplan', ['js.darg.api', 'xeditable']

app.controller 'OptionPlanController', ['$scope', '$http', 'OptionPlan', ($scope, $http, OptionPlan) ->

    $http.get('/services/rest/optionplan/' + optionplan_id).then (result) ->
        $scope.optionplan = new OptionPlan(result.data)
        $http.get($scope.optionplan.security).then (result1) ->
            $scope.optionplan.security = result1.data

    $http.get('/services/rest/security').then (result) ->
        $scope.securities = result.data.results

    # ATTENTION: django eats a url, angular eats an object.
    # hence needs conversion
    $scope.edit_company = () ->
        $scope.company.country = $scope.company.country.url
        $scope.company.$update().then (result) ->
            $scope.company = new Company(result)
            # refetch country data
            $http.get($scope.company.country).then (result1) ->
                $scope.company.country = result1.data

            console.log($scope.company)
        .then ->
            # Reset our editor to a new blank post
            #$scope.company = new Company()
            undefined
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data 

]

app.run (editableOptions) ->
  editableOptions.theme = 'bs3'
  # bootstrap3 theme. Can be also 'bs2', 'default'
  return
