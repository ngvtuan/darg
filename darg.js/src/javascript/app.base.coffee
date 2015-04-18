app = angular.module 'js.darg.app.base', ['js.darg.api',]

app.controller 'BaseController', ['$scope', '$http', ($scope, $http) ->
    @scope.test = True
]
