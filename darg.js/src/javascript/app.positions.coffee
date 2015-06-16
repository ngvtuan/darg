app = angular.module 'js.darg.app.positions', ['js.darg.api',]

app.controller 'PositionsController', ['$scope', '$http', 'Position', ($scope, $http, Position) ->
    $scope.positions = []
    $scope.shareholders = []

    $scope.show_add_position = false
    $scope.show_add_capital = false
    $scope.newPosition = new Position()

    $http.get('/services/rest/position').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.positions.push item

    $http.get('/services/rest/shareholders').then (result) ->
        angular.forEach result.data.results, (item) ->
            $scope.shareholders.push item

    $scope.add_position = ->
        $scope.newPosition.$save().then (result) ->
            $scope.positions.push result
        .then ->
            # Reset our editor to a new blank post
            $scope.newPosition = new Position()
        .then ->
            # Clear any errors
            $scope.errors = null
        , (rejection) ->
            $scope.errors = rejection.data

    $scope.show_add_position_form = ->
        $scope.show_add_position = true
        $scope.show_add_capital = false
        $scope.newPosition = new Position()

    $scope.show_add_capital_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = true
        $scope.newPosition = new Position()

    $scope.hide_form = ->
        $scope.show_add_position = false
        $scope.show_add_capital = false
        $scope.newPosition = new Position()

]
