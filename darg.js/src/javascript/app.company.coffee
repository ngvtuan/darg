app = angular.module 'js.darg.app.company', ['js.darg.api', 'xeditable']

app.controller 'CompanyController', ['$scope', '$http', 'Company', 'Country', 'Operator', ($scope, $http, Company, Country, Operator) ->

    $scope.operators = []
    $scope.company = null
    $scope.errors = null
    $scope.show_add_operator_form = false

    $scope.newOperator = new Operator()

    $http.get('/services/rest/company/' + company_id).then (result) ->
        $scope.company = new Company(result.data)
        $scope.company.founded_at = new Date($scope.company.founded_at)
        $http.get($scope.company.country).then (result1) ->
            $scope.company.country = result1.data

    $http.get('/services/rest/country').then (result) ->
        $scope.countries = result.data.results

    $http.get('/services/rest/operators').then (result) ->
        $scope.operators = result.data.results

    $scope.toggle_add_operator_form = () ->
        if $scope.show_add_operator_form
            $scope.show_add_operator_form = false
        else
            $scope.show_add_operator_form = true

    $scope.delete_operator = (pk) ->
        $http.delete('/services/rest/operators/'+pk)
        .then ->
            $http.get('/services/rest/operators').then (result) ->
                $scope.operators = result.data.results

    $scope.add_operator = () ->
        $scope.newOperator.company = $scope.company.url
        $scope.newOperator.$save().then (result) ->
            $http.get('/services/rest/operators').then (result) ->
                $scope.operators = result.data.results
        .then ->
            # reset form
            $scope.newOperator = new Operator()
        .then ->
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    # ATTENTION: django eats a url, angular eats an object.
    # hence needs conversion
    $scope.edit_company = () ->
        $scope.company.country = $scope.company.country.url
        $scope.company.founded_at = $scope.company.founded_at.toISOString().substring(0, 10)
        $scope.company.$update().then (result) ->
            result.founded_at = new Date(result.founded_at)
            $scope.company = new Company(result)
            # refetch country data
            $http.get($scope.company.country).then (result1) ->
                $scope.company.country = result1.data

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
