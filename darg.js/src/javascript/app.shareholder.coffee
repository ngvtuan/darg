app = angular.module 'js.darg.app.shareholder', ['js.darg.api',]

app.controller 'ShareholderController', ['$scope', '$http', ($scope, $http) ->
    $scope.test = true
]
