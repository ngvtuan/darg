app = angular.module 'js.darg.app.start', ['js.darg.api',]

app.controller 'StartController', ['$scope', '$http', 'Company', 'Shareholder', 'User', ($scope, $http, Company, Shareholder, User) ->

    # from server
    $scope.shareholders = [] #Shareholder.get().results
    $scope.user = [] #User.get().results

    # empty form data
    $scope.newShareholder = new Shareholder()
    $scope.newCompany = new Company()

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.shareholders.push item

    $http.get('/services/rest/user').then (result) ->
        $scope.user = result.data.results[0]

    $scope.add_company = ->
        $scope.newCompany.$save().then (result) ->
            $http.get('/services/rest/user').then (result) ->
                $scope.user = result.data.results[0]
                console.log($scope.user)
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
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.goto_shareholder = (shareholder_id) ->
        window.location = "/shareholder/"+shareholder_id+"/"
]
