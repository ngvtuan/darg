app = angular.module 'js.darg.app.company', ['js.darg.api',]

app.controller 'CompanyController', ['$scope', '$http', ($scope, $http) ->
    $scope.test = true
]
