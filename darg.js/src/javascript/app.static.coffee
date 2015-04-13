app = angular.module 'js.darg.app.static', []

app.controller 'AppController', ['$scope', '$http', ($scope, $http) ->
    $scope.shareholders = []
    $http.get('/services/rest/shareholders/').then (result) ->
            angular.forEach result.data.results, (item) ->
                $scope.shareholders.push item
]
