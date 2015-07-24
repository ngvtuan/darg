app = angular.module 'js.darg.app.company', ['js.darg.api', 'xeditable']

app.controller 'CompanyController', ['$scope', '$http', 'Company', 'Country', ($scope, $http, Company, Country) ->

    $http.get('/services/rest/company/' + company_id).then (result) ->
        $scope.company = new Company(result.data)
        $http.get($scope.company.country).then (result1) ->
            $scope.company.country = result1.data

    $http.get('/services/rest/country').then (result) ->
        $scope.countries = result.data.results

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
