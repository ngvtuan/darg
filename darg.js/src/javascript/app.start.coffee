app = angular.module 'js.darg.app.start', ['js.darg.api',]

app.controller 'StartController', ['$scope', '$http', 'Company', 'Shareholder', 'User', ($scope, $http, Company, Shareholder, User) ->

    $scope.shareholders = Shareholder.query().results
    $scope.user = User.query()

    $scope.newShareholder = new Shareholder()

    #$http.get('/services/rest/shareholders').then (result) ->
    #    angular.forEach result.data.results, (item) ->
    #        $scope.shareholders.push item



    $scope.add_company = ->
        $scope.company.$save().then (result) ->
            $scope.companies.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.company = new Company()
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.add_shareholder = ->
        $scope.newShareholder.$save().then (result) ->
            $scope.shareholders.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.newShareholder = new Shareholder()

]
